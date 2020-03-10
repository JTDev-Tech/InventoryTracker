"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from app.models import PackageModel, ContainerModel
from app.support import UnitManager

class FormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class PartAddSelectForm(forms.Form):
    """
    Allows the user to select a part to add
    """
    Part= forms.ChoiceField(choices=(
        ('n', 'Select Part'),
        ('r', 'Resistor'),
        ('c', 'Capacitor')))

    def __init__(self, *args, **kwargs):
        super(PartAddSelectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AddPartBase(FormBase):
    """
    Base class for adding a part
    """

    PartQuantity = forms.IntegerField(label='Quantity',
                                      help_text="Quantity of parts");

    Datasheet = forms.FileField(allow_empty_file=False, required=False)

    Package_ID = forms.ModelChoiceField(label='Package', queryset=PackageModel.objects.all())

    Container_ID = forms.ModelChoiceField(label='Container', queryset=ContainerModel.objects.all());

class ResistorForm(AddPartBase):
    """
    Form for adding a resistor
    """

    Value = forms.CharField(label='Value', max_length=30,
                            help_text='Resistor value')

    Unit = forms.ChoiceField(label="Unit", choices=UnitManager.ResistorChoices)

    ResistorToler = forms.ChoiceField(label='Tolerance', choices=(
        (0.05, "0.05%"),
        (0.1, "0.1%"),
        (0.25, "0.25%"),
        (0.5, "0.5%"),
        (1.0, "1%"),
        (2.0, "2%"),
        (5.0, "5%"),
        (10.0, "10%"),
        ))

    field_order = ['Value', 'Unit', 'PartQuantity',]

class CapacitorForm(AddPartBase):
    """
    Form to add a capacitor
    """
    Value = forms.FloatField(label='Value',
                            help_text='Cap value')

    Unit = forms.ChoiceField(label="Unit", choices=UnitManager.CapacitorChoices)

    Voltage = forms.FloatField(help_text="Voltage rating of the capacitor")

    field_order = ['Value', 'Unit', 'PartQuantity', 'Voltage',]