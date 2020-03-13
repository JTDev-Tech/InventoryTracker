from django.test import Client, TestCase

from app.models import PartModel, PackageModel, PartCategoryModel, ShelfModel, ContainerModel

class TestAddPart(TestCase):
    def setUp(self):
        self.__Shelf = ShelfModel.objects.create(Name="Test Shelf", LocationID="Unknown")
        self.__Container = ContainerModel.objects.create(Name="Test Container", LocationID="Unknown", Shelf=self.__Shelf)
        self.__Package = PackageModel.objects.create(Name='0805', Reference='None.local')
        return

    def test_GetAddPartPage(self):
        """
        Test we can get the basic add part page
        """
        c= Client()
        Resp = c.get('/add_part')
        self.assertEqual(200, Resp.status_code)
        return

    def test_GetAddPartPageCap(self):
        """
        Make a get request to the add capacitor page
        """
        c= Client()
        Resp = c.get('/add_part/c')
        self.assertEqual(200, Resp.status_code)
        return

    def test_GetAddPartPageRes(self):
        """
        Make a get request to the add resistor page
        """
        c= Client()
        Resp = c.get('/add_part/c')
        self.assertEqual(200, Resp.status_code)
        return

    def test_AddCapacitor(self):
        """
        Make sure we can add a capacitor
        """
        c = Client()
        Resp = c.post('/add_part/c', {'PartQuantity':10, 
                                      'Package_ID':self.__Package.pk,
                                      'Container_ID':self.__Container.pk,
                                      'Value':10,
                                      'Unit':203,
                                      'Voltage':25})

        self.assertEqual(200, Resp.status_code)

        part:PartModel = PartModel.objects.get(Value = 10)

        self.assertEqual(part.Value, 10)
        self.assertEqual(part.GetValue(), '10nF')
        return

    def test_AddCapacitor(self):
        """
        Make sure we can add a capacitor
        """
        c = Client()
        Resp = c.post('/add_part/r', {'PartQuantity':10, 
                                      'Package_ID':self.__Package.pk,
                                      'Container_ID':self.__Container.pk,
                                      'Value':20,
                                      'Unit':101,
                                      'ResistorToler':10.0})

        self.assertEqual(200, Resp.status_code)

        part:PartModel = PartModel.objects.get(Value = 20)

        self.assertEqual(part.Value, 20)
        self.assertEqual(part.GetValue(), '20KΩ')
        return
