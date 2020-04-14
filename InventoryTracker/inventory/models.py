"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum, Q
from .support import UnitManager
from .support import CommonAttrNames

class PackageModel(models.Model):
    """
    Packages a part can take. For example 0805 for resister
    """
    Name = models.CharField(max_length=256, unique=True,
                            help_text="Name of this package")

    Reference = models.URLField(help_text="Link to reference documentation for this parts package")

    class Meta:
        verbose_name = 'Footprint'

    def __str__(self):
        return self.Name

class PartCategoryModel(models.Model):
    """
    Part classification.
    """
    CategoryName = models.CharField(max_length=256,
                                    help_text="Name of this part classification")

    Parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank = True,
                               help_text="Parent category, if any")

    class Meta:
        verbose_name = 'Part Category'
        unique_together = [['CategoryName', 'Parent']]

    def __str__(self):
        return self.CategoryName

class ShelfModel(models.Model):
    '''
    Defines a shelf that can hold containers full of parts
    '''
    Name = models.CharField(max_length=256)

    LocationID = models.CharField(max_length=32, unique=True,
                                  help_text="User assigned location ID for this shelf")

    class Meta:
        verbose_name = 'Shelf'

    def __str__(self):
        return self.Name

class ContainerModel(models.Model):
    """
    Containers sit on shelfs, and are full of parts
    """
    Name = models.CharField(max_length=256)

    LocationID = models.CharField(max_length=32,
                                  help_text="User assigned location ID for this container")

    Shelf =models.ForeignKey(ShelfModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Container'
        unique_together = [['LocationID', 'Shelf'], ['LocationID', 'Name']]

    def __str__(self):
        return self.Name

class PartAttrModel(models.Model):
    """
    Attribute that can be assigned to a part
    """
    Name = models.CharField(max_length=256,
                            help_text="Name assigned to this attribute")

    Value = models.CharField(max_length=256,
                             help_text="Value of this attribute")

    class Meta:
        verbose_name = 'Part Attribute'
        unique_together = [['Name', 'Value']]

    def __str__(self):
        return self.Name + "=" + self.Value

class PartModel(models.Model):
    """
    This is an actual electronic part
    """
    Name = models.CharField(max_length=256,
                            help_text="Name of the electronic part")

    Value = models.FloatField(blank=True, null=True,
        help_text = "Value for this part")

    MfgName = models.CharField(max_length=128, blank=True,
                               help_text="Name of the part manufactor")

    MfgPartNumber = models.CharField(max_length=128, blank=True,
                                     help_text='Manufactorers part number for this part')

    DataSheet = models.FileField(upload_to='data_sheets/%m/', null=True, blank=True,
                                 help_text="Datasheet for this part")

    PreviewImage = models.ImageField(upload_to='preview_img/%m/', null=True, blank=True,
                                     help_text="Preview image for this part")

    Package = models.ForeignKey(PackageModel, on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Package of this part")

    Category = models.ForeignKey(PartCategoryModel, on_delete=models.CASCADE)

    Attributes = models.ManyToManyField(PartAttrModel, blank= True,
                            help_text="Part this attribute is assigned to")

    class Meta:
        verbose_name = 'Part'

    def GetValue(self):
        Res = self.Name
        try:
            ValueUnitID = self.Attributes.get(Name = CommonAttrNames.ValueUnit)
            Unit = UnitManager.GetUnitFromID(int(ValueUnitID.Value))
            Res = '{:-n}{}'.format(self.Value, Unit.Designator)
        except PartAttrModel.DoesNotExist:
            #No value unit present
            pass
        except ValueError:
            #This might be thrown of ValueUnit attribute has a value other then a number
            pass

        return Res

    def GetAvailable(self):
        """
        Get the total number of parts available across all containers
        """
        s = self.partcountmodel_set.aggregate(Sum('Quantity'))
        A = s['Quantity__sum']
        if A is None:
            A = 0
        return int(A)

    def __str__(self):
        return self.GetValue()
        

class PartCountModel(models.Model):
    """
    Count of a part
    """
    Quantity = models.IntegerField(help_text="Part quantity")

    Bin = models.CharField(max_length=32, blank=True,
                           help_text="Bin ID this part is stored in")

    Location = models.ForeignKey(ContainerModel, on_delete=models.CASCADE,
                                 help_text="Location of these parts")

    Part = models.ForeignKey(PartModel, on_delete=models.CASCADE,
                             help_text="Part this count is for")

    class Meta:
        verbose_name = 'Part Count'
        unique_together = [['Location', 'Part']]

    def __str__(self)->str:
        return '{}{:-n}'.format(self.Part.Name, self.Quantity)

