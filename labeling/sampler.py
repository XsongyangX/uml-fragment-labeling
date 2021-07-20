# Chooses data samples

from .models import Model, Fragment

class Sampler:
    
    smallest_class_count = 1
    largest_class_count = Model.objects.order_by("-classes").first().classes

    @staticmethod
    def next():
        """Picks the next smallest model whose labeling is the closest to completion.
        Return None, None if all is done.
        """
        model = Sampler.more_models(1)
        if model == None:
            return None, None
        else:
            model = model.get()
        fragment: Fragment = Fragment.objects.filter(model=model, label__isnull=True).order_by("number").first()
        return model, fragment

    @staticmethod
    def more_models(limit: int):
        """Returns a list of at most <limit> unfinished models
        """
        probing_size = Sampler.smallest_class_count
        models = Model.objects.filter(classes=probing_size, fragment__label__isnull=True)[:limit]

        while len(models) == 0:
            probing_size += 1
            models = Model.objects.filter(classes=probing_size, fragment__label__isnull=True)[:limit]

            # all finished labeling
            if probing_size > Sampler.largest_class_count:
                return None

        return models