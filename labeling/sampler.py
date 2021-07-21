# Chooses data samples

from .models import Model, Fragment

class Sampler:
    
    current_class_count = 1
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
            model = model[0]
        fragment: Fragment = Fragment.objects.filter(model=model, label__isnull=True).order_by("number").first()
        return model, fragment

    @staticmethod
    def more_models(limit: int):
        """Returns a list of at most <limit> unfinished models
        """
        probing_size = Sampler.current_class_count
        models = Model.objects.filter(classes__gte=probing_size, fragment__label__isnull=True).distinct().order_by("classes")[:limit]

        return models