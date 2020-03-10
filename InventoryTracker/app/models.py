"""
Definition of models.
"""

from django.db import models
from app.support import UnitManager

class PackageModel(models.Model):
    """
    Packages a part can take. For example 0805 for resister
    """
    Name = models.CharField(max_length=256, unique=True,
                            help_text="Name of this package")

    Reference = models.URLField(help_text="Link to reference documentation for this parts package")

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
        unique_together = [['CategoryName', 'Parent']]

    def __str__(self):
        return self.CategoryName

# Create your models here.
class ShelfModel(models.Model):
    '''
    Defines a shelf that can hold containers full of parts
    '''
    Name = models.CharField(max_length=256)

    LocationID = models.CharField(max_length=32, unique=True,
                                  help_text="User assigned location ID for this shelf")

    def __str__(self):
        return self.Name

    def ToJsonDict(self):
        """
        Converts the model to a dictionary suitable for conversion to JSON
        """

        return {"ID":self.pk, "Name":self.Name, "LocationID":self.LocationID}


class ContainerModel(models.Model):
    """
    Containers sit on shelfs, and are full of parts
    """
    Name = models.CharField(max_length=256)

    LocationID = models.CharField(max_length=32,
                                  help_text="User assigned location ID for this container")

    Shelf =models.ForeignKey(ShelfModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['LocationID', 'Shelf'], ['LocationID', 'Name']]

    def ToJsonDict(self):
        """
        Converts the model to a dictionary suitable for conversion to JSON
        """
        return {"ID":self.pk, "Name":self.Name, "LocationID":self.LocationID, "Shelf":self.Shelf.ToJsonDict()}

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
        unique_together = [['Name', 'Value']]

    def __str__(self):
        return self.Name + "=" + self.Value


class PartModel(models.Model):
    """
    This is an actual electronic part
    """
    Name = models.CharField(max_length=256,
                            help_text="Name of the electronic part")

    Value = models.IntegerField(blank=True, null=True,
        help_text = "Value for this part")

    MfgPartNumber = models.CharField(max_length=128, blank=True,
                                     help_text='Manufactorers part number for this part')

    UnitID = models.IntegerField(null=True, blank=True)

    DataSheet = models.FileField(upload_to='data_sheets/%m/', null=True, blank=True,
                                 help_text="Datasheet for this part")

    Package = models.ForeignKey(PackageModel, on_delete=models.CASCADE,
                                help_text="Package of this part")

    Category = models.ForeignKey(PartCategoryModel, on_delete=models.CASCADE)

    Attributes = models.ManyToManyField(PartAttrModel, blank= True,
                            help_text="Part this attribute is assigned to")

    class Meta:
        unique_together = [['Value', 'UnitID']]

    def __str__(self):
        unit = UnitManager.GetUnitFromID(self.UnitID)
        Unitfix = ""
        if unit is not None:
            Unitfix = unit.Designator

        return "%s%s(%s)" % (self.Value, Unitfix, self.Package.Name)

class PartCountModel(models.Model):
    """
    Count of a part
    """
    Quantity = models.IntegerField(help_text="Part quantity")

    Location = models.ForeignKey(ContainerModel, on_delete=models.CASCADE,
                                 help_text="Location of these parts")

    Part = models.ForeignKey(PartModel, on_delete=models.CASCADE,
                             help_text="Part this count is for")

    class Meta:
        unique_together = [['Location', 'Part']]

    def __str__(self)->str:
        return "%s(%i)" % (self.Part.Name, self.Quantity)