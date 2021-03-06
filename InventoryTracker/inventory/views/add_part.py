from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Length
from django.urls import reverse
from django.views.generic.base import TemplateView
import django.db.utils

from inventory.forms import ResistorForm, PartAddSelectForm, AddPartBase, CapacitorForm
from inventory.models import PartModel, PartCountModel, ContainerModel
from inventory.models import PackageModel, PartCategoryModel, PartAttrModel

from inventory.support.units import UnitManager
from inventory.support import CommonAttrNames

class AddPartBaseView(TemplateView):
    """
    Base view class for adding a part
    """
    template_name = "inventory/add_part.html"

    def __init__(self, **kwargs):
        self._Form = None
        self.ErrorText = None
        self.SuccessText = None
        return super().__init__(**kwargs)

    def GetPartTypeForm(self):
        return PartAddSelectForm()

    def GetURL(self):
        return reverse('inventory:add_part')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.GetURL()
        context['Form'] = self._Form
        context['title'] = "Add Part"
        context['PartForm'] = self.GetPartTypeForm()
        context['ErrorText'] = self.ErrorText
        context['SuccessText'] = self.SuccessText
        context['BaseURL'] = reverse('inventory:add_part')
        return context

def _GetCategory(name:str) -> PartCategoryModel:
    """
    Get a category by name. Or create it if it doesn't exist
    """
    try:
        return PartCategoryModel.objects.get(CategoryName=name)
    except PartCategoryModel.DoesNotExist:
        new = PartCategoryModel(CategoryName=name)
        new.save()
        return new

def _GetAttr(name:str, value:str) -> PartAttrModel:
    """
    """
    (obj, c) = PartAttrModel.objects.get_or_create(Name=name, Value=value)

    return obj

def _GetParts(form:AddPartBase, cat:str):
    """
    Extract the container and Package for a part to add
    """
    Cont = form.cleaned_data["Container_ID"]
    Pack = form.cleaned_data['Package_ID']
    Cat = _GetCategory(cat)

    return (Cont, Pack, Cat)

class AddResistorView(AddPartBaseView):
    """
    View class to add a resistor
    """
    def post(self, request:HttpRequest, *args, **kwargs):
        self._Form = ResistorForm(request.POST, request.FILES)

        if self._Form.is_valid():
            try:
                with transaction.atomic():
                    UnitID = self._Form.cleaned_data['Unit']
                    Cont, Pack, Cat = _GetParts(self._Form, "Resistor")
                    Tol = _GetAttr(CommonAttrNames.Tolerance, self._Form.cleaned_data["ResistorToler"])
                    ValueUnit = _GetAttr(CommonAttrNames.ValueUnit, UnitID)

                    PM = PartModel(Name=self._Form.cleaned_data['Value'],
                                   Value = self._Form.cleaned_data['Value'],
                                   Package = Pack,
                                   Category = Cat)

                    if 'Datasheet' in self._Form.cleaned_data:
                        PM.DataSheet = self._Form.cleaned_data['Datasheet']

                    if 'PreviewImage' in self._Form.cleaned_data:
                        PM.PreviewImage = self._Form.cleaned_data['PreviewImage']

                    PM.save()
                    PM.Attributes.add(Tol)
                    PM.Attributes.add(ValueUnit)
                    PM.save()
                    PartQuantity = self._Form.cleaned_data['PartQuantity']
                    if PartQuantity > 0:
                        PC = PartCountModel(Quantity=PartQuantity,
                                            Location=Cont,
                                            Part=PM)
                        PC.save()

                    self._Form.errors.clear()
                    self.SuccessText = "Resistor %s(%s) added" % (PM.GetValue(), PM.Package.Name)
            except django.db.utils.IntegrityError:
                self.ErrorText = "Part already exists"

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self._Form = ResistorForm()
        return super().get(request, *args, **kwargs)

    def GetPartTypeForm(self):
        return PartAddSelectForm({'Part':'r'})

    def GetURL(self):
        return super().GetURL() + "/r"

class AddCapacitorView(AddPartBaseView):
    """
    View that allows adding a capacitor
    """

    def post(self, request:HttpRequest, *args, **kwargs):
        self._Form = CapacitorForm(request.POST, request.FILES)

        if self._Form.is_valid():
            try:
                with transaction.atomic():
                    Cont, Pack, Cat = _GetParts(self._Form, "Capacitor")
                    Tol = _GetAttr(CommonAttrNames.Voltage, self._Form.cleaned_data["Voltage"])
                    ValueUnit = _GetAttr(CommonAttrNames.ValueUnit, self._Form.cleaned_data['Unit'])

                    PM = PartModel(Name=self._Form.cleaned_data['Value'],
                                   Value = self._Form.cleaned_data['Value'],
                                   Package = Pack,
                                   Category = Cat)

                    if 'Datasheet' in self._Form.cleaned_data:
                        PM.DataSheet = self._Form.cleaned_data['Datasheet']

                    if 'PreviewImage' in self._Form.cleaned_data:
                        PM.PreviewImage = self._Form.cleaned_data['PreviewImage']

                    PM.save()
                    PM.Attributes.add(Tol)
                    PM.Attributes.add(ValueUnit)
                    PM.save()

                    PartQuantity = self._Form.cleaned_data['PartQuantity']
                    if PartQuantity > 0:
                        PC = PartCountModel(Quantity=self._Form.cleaned_data['PartQuantity'],
                                            Location=Cont,
                                            Part=PM)
                        PC.save()
                    
                    self._Form.errors.clear()
                    self.SuccessText = "Capacitor %s(%s) added" % (PM.GetValue(), PM.Package.Name)
            except django.db.utils.IntegrityError:
                self.ErrorText = "Part already exists"

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self._Form = CapacitorForm()
        return super().get(request, *args, **kwargs)

    def GetPartTypeForm(self):
        return PartAddSelectForm({'Part':'c'})

    def GetURL(self):
        return super().GetURL() + "/c"
