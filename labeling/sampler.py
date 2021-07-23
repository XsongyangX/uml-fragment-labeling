# Chooses data samples

from typing import List, Union
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from .models import Model, Fragment

import threading


def block(duration):
    def sleep_and_remove(reserved_data: Union[Fragment, Model], condition: threading.Condition):
        condition.acquire()
        condition.wait(timeout=duration)
        del Sampler.recently_assigned[str(reserved_data)]
        condition.release()

    def wrapper(func):
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)

            # returning from next(), only reserve the fragment
            if isinstance(result, tuple) and len(result) == 2:
                _, fragment = result

                # check for existing reservation, do nothing if so
                if str(fragment) in Sampler.recently_assigned:
                    return result

                condition = threading.Condition()
                Sampler.recently_assigned[str(fragment)] = {
                    "data_object": fragment,
                    "thread_condition": condition,
                }
                threading.Thread(target=sleep_and_remove,
                                 args=(fragment, condition),
                                 name=str(fragment)).start()

            # returning a single model
            elif isinstance(result, Model):
                # check for existing reservation, do nothing if so
                if str(result) in Sampler.recently_assigned:
                    return result

                condition = threading.Condition()
                Sampler.recently_assigned[str(result)] = {
                    "data_object": result,
                    "thread_condition": condition
                }
                threading.Thread(target=sleep_and_remove,
                                 args=(result, condition),
                                 name=str(result)).start()

            # returning from more_fragments()
            elif isinstance(result, QuerySet) and all([isinstance(x, Fragment) for x in result]):
                for fragment in result:
                    # check for existing reservation, do nothing if so
                    if str(fragment) in Sampler.recently_assigned:
                        return result
                    condition = threading.Condition()
                    Sampler.recently_assigned[str(fragment)] = {
                        "data_object": fragment,
                        "thread_condition": condition,
                    }
                    threading.Thread(target=sleep_and_remove,
                                     args=(fragment, condition),
                                     name=str(fragment)).start()

            # block one fragment
            elif isinstance(result, Fragment):
                
                fragment = result
                if str(fragment) in Sampler.recently_assigned:
                        return result
                condition = threading.Condition()
                
                Sampler.recently_assigned[str(fragment)] = {
                    "data_object": fragment,
                    "thread_condition": condition,
                }
                threading.Thread(target=sleep_and_remove,
                                    args=(fragment, condition),
                                    name=str(fragment)).start()

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
        if isinstance(element, Fragment) and query.model.__name__ == 'Fragment':
            return query.exclude(kind=element.kind, number=element.number, model=element.model)
        elif isinstance(element, Model):
            if query.model.__name__ == 'Fragment':
                return query.exclude(model__name=element.name)
            else:
                return query.exclude(name=element.name)
        else:
            return query

    @staticmethod
    def excluding_reserved(query: BaseManager):
        for excluded in Sampler.recently_assigned.keys():
            query = Sampler.exclude_one(query, Sampler.recently_assigned[excluded]["data_object"])
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
        models = Model.objects.filter(
            classes__gte=1, fragment__label__isnull=True)

        if exclude is not None:
            models = models.exclude(name=exclude.name)

        models = Sampler.excluding_reserved(models)

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
    # one item ex: Fragment
    #   "Person_class0": {
    #       "data_object": fragment_object_from_django,
    #       "thread_condition": condition_object_of_sleeper_thread
    #   }
    recently_assigned = {}

    @staticmethod
    def free(data: Union[Model, Fragment]):
        assigned = Sampler.recently_assigned[str(data)]
        condition : threading.Condition = assigned["thread_condition"]
        condition.acquire()
        try:
            condition.notify()
        finally:
            condition.release()

    @staticmethod
    def free_fragments(fragments: List[Fragment]):
        for f in fragments:
            # also frees the associated model if possible
            if str(f.model) in Sampler.recently_assigned:
                Sampler.free(f.model)
            Sampler.free(f)
    
    @staticmethod
    def free_all():
        for element in Sampler.recently_assigned.keys():
            assigned = Sampler.recently_assigned[element]
            condition : threading.Condition = assigned["thread_condition"]
            condition.acquire()
            try:
                condition.notify()
            finally:
                condition.release()