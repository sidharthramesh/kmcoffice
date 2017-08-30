from django.test import TestCase
from .gcalander import get_classes
# Create your tests here.
class GcalTest(TestCase):
    def test_classes(self):
        classes = get_classes(2017,8,31)
        self.assertEqual(len(classes),5)
        self.assertIsNotNone(classes[0].get('department'))
        self.assertEqual(classes[0].get('department'),'Pharmacology')
        self.assertIsNotNone(classes[0].get('location'))
