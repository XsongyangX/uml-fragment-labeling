from labeling.models import Fragment, Model
from django.test import TestCase

# Create your tests here.
from labeling.sampler import Sampler
class SamplerTestCase(TestCase):

    def setUp(self) -> None:
        m = Model.objects.create(name="Person", classes=1, relations=0)
        Fragment.objects.create(kind="class", number=0, model=m, unique_id=0)
        m2 = Model.objects.create(name="MKML", classes=2, relations=0)
        Fragment.objects.create(model=m2, kind="class", number=0, unique_id=1)

    def test_exclusion(self):
        m = Model.objects.first()
        q = Fragment.objects.filter(model=m, kind="class", number=0)
        self.assertEqual(len(q), 1)
        exclusion = Sampler.exclude_one(q, Fragment.objects.get(model=m, kind="class", number=0))
        self.assertEqual(len(exclusion), 0)

    def test_simultaneous_query(self):
        model, fragment = Sampler.next()
        model2, fragment2 = Sampler.next()
        self.assertIsNotNone(fragment)
        self.assertIsNotNone(fragment2)
        self.assertNotEqual(fragment, fragment2)