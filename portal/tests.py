from django.test import TestCase
from portal.models import testpost

class SimpleTest(TestCase):
    def setUp(self):
        testpost(content='Tesss hahah').save()

    def test_setup(self):
        self.assertEqual(1, len(testpost.objects.all()))
        self.assertEqual('weee', testpost.objects.all()[0].content)
