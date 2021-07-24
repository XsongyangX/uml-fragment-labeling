import json
import threading

from django.db.models.fields import SmallIntegerField
from labeling.models import Fragment, Model
from django.test import TestCase

# Create your tests here.
from labeling.sampler import Sampler
class SamplerTestCase(TestCase):

    def setUp(self) -> None:
        m = Model.objects.create(name="Person", classes=2, relations=1)
        Fragment.objects.create(kind="class", number=0, model=m, unique_id=0)
        Fragment.objects.create(kind="class", number=1, model=m, unique_id=1)
        Fragment.objects.create(kind="rel", number=0, model=m, unique_id=2)
        m2 = Model.objects.create(name="MKML", classes=2, relations=2)
        Fragment.objects.create(model=m2, kind="class", number=0, unique_id=3)
        Fragment.objects.create(model=m2, kind="class", number=1, unique_id=4)
        Fragment.objects.create(model=m2, kind="rel", number=0, unique_id=5)
        Fragment.objects.create(model=m2, kind="rel", number=1, unique_id=6)

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
        self.assertNotEqual(len(Sampler.recently_assigned), 0)

        # freeing
        Sampler.free(fragment)
        Sampler.free(fragment2)
        threading.Event().wait(0.01)
        self.assertEqual(len(Sampler.recently_assigned), 0)

    def test_more_models(self):
        models = Sampler.more_models(5)
        self.assertEqual(len(models), 2)

    def test_more_fragments(self):
        fragments = Sampler.more_fragments(model=Model.objects.get(name="Person"), limit=5)
        self.assertEqual(len(fragments), 3)
        Sampler.free_fragments(fragments)
        threading.Event().wait(0.01)

class TestViews(TestCase):
    def setUp(self) -> None:
        return SamplerTestCase().setUp()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "umllabels/index.html")
        
        self.assertEqual(response.context.get("total_models"), 2)
        self.assertEqual(response.context.get("fragments_done"), 0)
        self.assertEqual(response.context.get("total_fragments"), 7)
        self.assertEqual(response.context.get("models_done"), 0)
        
    def test_labeling_page(self):
        response = self.client.get('/labeling/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labeling/index.html")
        self.assertNotEqual(len(Sampler.recently_assigned), 0)

        Sampler.free_all()
        threading.Event().wait(0.01)
        self.assertEqual(len(Sampler.recently_assigned), 0)

    def test_two_labeling_pages(self):
        response = self.client.get('/labeling/')
        response2 = self.client.get('/labeling/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labeling/index.html")
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "labeling/index.html")

        self.assertNotEqual(response.context.get("shown_fragment"), response2.context.get("shown_fragment"))

        Sampler.free_all()
        threading.Event().wait(0.01)
        self.assertEqual(len(Sampler.recently_assigned), 0)