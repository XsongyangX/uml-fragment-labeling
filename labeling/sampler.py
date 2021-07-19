# Chooses data samples

from typing import Tuple
from .models import Model, Fragment

class Sampler:
    
    def next():
        """Picks the next smallest model whose labeling is closest to completion
        """
        model: Model = Model.objects.get(name="COBOL")
        fragment: Fragment = Fragment.objects.get(model=model, kind="class", number="0")
        return model, fragment