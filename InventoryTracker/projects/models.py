from django.db import models
from django.db.models import Sum, Q

# Create your models here.
class ProjectModel(models.Model):
    """
    Represents a project that will consume parts
    """
    Name = models.CharField(max_length=128,
                            help_text='Name of this project')

    Description = models.TextField(help_text="Description for this project")

    class Meta:
        verbose_name = 'Project'

    def __str__(self):
        return self.Name

class ProjectPartModel(models.Model):
    """
    Links a part to a project.
    """

    Quantity = models.IntegerField(help_text='Quantity of parts required')

    Part = models.ForeignKey('inventory.PartModel', on_delete=models.CASCADE,
                             help_text="Part required")

    Project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE,
                                help_text='Project this part is required for')

    class Meta:
        verbose_name = 'Project Part'
        unique_together=['Part', 'Project']

    def __str__(self):
        return '{} - {}'.format(self.Part, self.Project)

    def GetDesignators(self):
        """
        Get a list of designators separated by comma
        """
        d = self.bomdesignatormodel_set.all()
        return ','.join([str(x) for x in d])

class BOMDesignatorModel(models.Model):
    """
    This is a designator that is applied to a project part.
    For example U2 or R7
    """

    Number = models.IntegerField(help_text='Numeric part of the designator')

    Letter = models.CharField(max_length=2,
                              help_text="Letter part of the designator")

    PartModel = models.ForeignKey(ProjectPartModel, on_delete=models.CASCADE,
                                  help_text='Project part this designator is applied to')

    class Meta:
        verbose_name='Part Designator'
        constraints = [
            models.UniqueConstraint(fields=['Number', 'Letter', 'PartModel'], name='BOMNumberLetterPartConstrant'),
            models.CheckConstraint(check=Q(Number__gte=0), name='BOMNumbergte0')
        ]

    def __str__(self):
        return self.Letter + str(self.Number)