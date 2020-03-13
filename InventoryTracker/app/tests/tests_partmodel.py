from django.test import TestCase

from app.models import PartModel, PackageModel, PartCategoryModel, ShelfModel

class PartModelTests(TestCase):
    def setUp(self):
        shelf = ShelfModel.objects.create(Name='Workbench', LocationID='Workbench')
        r = PartCategoryModel.objects.create(CategoryName="Resistor")
        s = PartCategoryModel.objects.create(CategoryName="Screw")
        p = PackageModel.objects.create(Name='0805', Reference='none.local')

        PartModel.objects.create(Name='TXB0102', Package=p, Category=r)
        

    def test_Str(self):
        """
        Make sure the string method works without any issues
        """
        all = PartModel.objects.all()
        self.assertGreaterEqual(len(all), 1)
        for x in all:
            s = str(x)
            self.assertIsNotNone(s)
            self.assertGreaterEqual(len(s), 1)
        return

    def test_GetValueNoValueUnit(self):
       P:PartModel = PartModel.objects.get(Name='TXB0102')
       v = P.GetValue();
       self.assertIsNotNone(v)
       self.assertGreaterEqual(len(v), 1)