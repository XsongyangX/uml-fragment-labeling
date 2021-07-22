# Chooses data samples

from typing import Union
from django.db.models.manager import BaseManager
from .models import Model, Fragment

import threading


def block(duration):
    def sleep_and_remove(reserved_data):
        e = threading.Event()
        e.wait(timeout=duration)

        Sampler.recently_assigned.remove(reserved_data)

    def wrapper(func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)

            # returning from next(), only reserve the fragment
            if isinstance(result, tuple) and len(result) == 2:
                _, fragment = result
                Sampler.recently_assigned.append(fragment)
                threading.Thread(target=sleep_and_remove,
                                 args=(fragment,)).start()

            # returning a single model
            elif isinstance(result, Model):
                Sampler.recently_assigned.append(result)
                threading.Thread(target=sleep_and_remove,
                                 args=(result, )).start()

            # returning from more_fragments()
            elif isinstance(result, BaseManager) and all([isinstance(x, Fragment) for x in result]):
                for fragment in result:
                    Sampler.recently_assigned.append(fragment)
                    threading.Thread(target=sleep_and_remove,
                                     arg=(fragment, )).start()

            # during None and exception returns, do nothing
            else:
                pass

            return result
        return wrapped
    return wrapper


class Sampler:

    current_class_count = 1
    largest_class_count = Model.objects.order_by("-classes").first().classes

    @staticmethod
    def exclude_one(query: BaseManager, element: Union[Fragment, Model]):
        if isinstance(element, Fragment) and isinstance(query.model, Fragment):
            return query.exclude(kind=element.kind, number=element.number)
        elif isinstance(element, Model):
            if isinstance(query.model, Fragment):
                return query.exclude(model__name=element.name)
            else:
                return query.exclude(name=element.name)
        else:
            return query

    @staticmethod
    def excluding_reserved(query: BaseManager):
        for excluded in Sampler.recently_assigned:
            query = Sampler.exclude_one(query, excluded)
        return query

    @staticmethod
    @block(60)
    def next():
        """Picks the next smallest model whose labeling is the closest to completion.
        Return None, None if all is done.
        """
        model = Sampler.more_models(1)
        if len(model) == 0:
            return None, None
        else:
            model = model.first()

        fragment = Sampler.excluding_reserved(
            Fragment.objects.filter(
                model=model, label__isnull=True)
        )

        if len(fragment) == 0:
            # block this model
            @block(60)
            def this_model(): return model
            this_model()
            # get a new one
            return Sampler.next()

        return model, fragment.order_by("number").first()

    @staticmethod
    def more_models(limit: int, exclude=None):
        """Returns a list of at most <limit> unfinished models
        """
        models = Model.objects.filter(classes__gte=1, fragment__label__isnull=True)

        if exclude is not None:
            models = models.exclude(name=exclude.name)

        return models.distinct().order_by("classes")[:limit]

    @staticmethod
    @block(60)
    def more_fragments(model: Model, limit: int):
        """Returns a list of at most <limit> unlabeled fragments of the model

        Args:
            model (Model): Model to get fragments from
            limit (int): How many fragments at most to get
        """
        fragments = Fragment.objects.filter(model=model, label__isnull=True)
        fragments = Sampler.excluding_reserved(fragments)
        return fragments.order_by("number")[:limit]

    # Concurrency
    # Ensure that simultaneous users get different things to work on
    recently_assigned = []
