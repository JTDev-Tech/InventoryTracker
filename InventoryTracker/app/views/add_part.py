from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Length
from django.urls import resolve

from app.forms import ResistorForm, PartAddSelectForm, AddPartBase, CapacitorForm
from app.models import PartModel, PartCountModel, ContainerModel
from app.models import PackageModel, PartCategoryModel, PartAttrModel
from app.models import MeasurementUnitModel

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

def _MakeForm(request, form):
    if request.method == "POST":
        return form(request.POST)
    else:
        return form

def _GetResValue(value:str, cat:PartCategoryModel):
    """
    Given a value, with a unit postfix, convert that to a value measurement
    """
    Units = MeasurementUnitModel.objects.filter(PartCategory = cat)

    if value[-1].isalpha():
        #We have a unit postfix on the value
        l = value[-1:].upper()
        u = Units.get(Q(Postfix__startswith=l))
        return (value[:-1], u)
        
    else:
        #No unit postfix, assume baseless
        u = Units.annotate(length=Length('Postfix')).get(length=1)
        return (value, u)

def _GetParts(form:AddPartBase, cat:str):
    """
    Extract the container and Package for a part to add
    """
    Cont = form.cleaned_data["Container_ID"]
    Pack = form.cleaned_data['Package_ID']
    Cat = _GetCategory(cat)

    return (Cont, Pack, Cat)

def add_part(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    return render(request,
        'app/add_part.html',
        {
            'url':'/add_part',
            'Form':None,
            'PartForm':PartAddSelectForm(),
            'title':'Add Part',
        })

def add_part_capacitor(request:HttpRequest):
    """
    Add a capacitor
    """
    ErrorText:str = None
    SuccessText:str = None
    Form = CapacitorForm

    if request.method == 'POST':
        Form = CapacitorForm(request.POST, request.FILES)
        if Form.is_valid():
            try:
                with transaction.atomic():
                    Cont, Pack, Cat = _GetParts(Form, "Capacitor")
                    Value, Unit = _GetResValue(Form.cleaned_data['Value'], Cat)
                    Vol = _GetAttr("Voltage", Form.cleaned_data["Voltage"])

                    print(Value)

                    PM = PartModel(Name=Form.cleaned_data['Value'],
                                   Value = Value,
                                   Unit = Unit,
                                   Package = Pack,
                                   Category = Cat)

                    if 'Datasheet' in Form.cleaned_data:
                        PM.DataSheet = Form.cleaned_data['Datasheet']

                    PM.save()
                    PM.Attributes.add(Vol)
                    PM.save()

                    PC = PartCountModel(Quantity=Form.cleaned_data['PartQuantity'],
                                        Location=Cont,
                                        Part=PM)

                    PC.save()
            except:
                raise

    return render(request,
        'app/add_part.html',
        {
            "ErrorText":ErrorText,
            "SuccessText":SuccessText,
            'url':request.path_info,
            'Form':Form,
            'PartForm':PartAddSelectForm({'Part':'c'}),
            'title':'Add Part',
        })

def add_part_resistor(request):
    """
    Add a resistor
    """
    ErrorText:str = None
    SuccessText:str = None

    if request.method == 'POST':
        Form = ResistorForm(request.POST, request.FILES)

        if Form.is_valid():
            try:
                with transaction.atomic():
                    Cont, Pack, Cat = _GetParts(Form, "Resistor")
                    Tol = _GetAttr("tolerance", Form.cleaned_data["ResistorToler"])
                    Value, Unit = _GetResValue(Form.cleaned_data['Value'], Cat)

                    PM = PartModel(Name=Form.cleaned_data['Value'],
                                   Value = Value,
                                   Unit = Unit,
                                   Package = Pack,
                                   Category = Cat)

                    if 'Datasheet' in Form.cleaned_data:
                        PM.DataSheet = Form.cleaned_data['Datasheet']

                    PM.save()
                    PM.Attributes.add(Tol)
                    PM.save()

                    PC = PartCountModel(Quantity=Form.cleaned_data['PartQuantity'],
                                        Location=Cont,
                                        Part=PM)

                    PC.save()
                    
                    Form = ResistorForm({'ResistorToler':Form.cleaned_data["ResistorToler"],
                                         'Package_ID':Form.cleaned_data['Package_ID'],
                                         'Container_ID':Form.cleaned_data["Container_ID"]})
                    Form.errors.clear()
                    SuccessText = "Part added"
            except MeasurementUnitModel.DoesNotExist:
                ErrorText = "Invalid value unit"
    else:
        Form = ResistorForm

    return render(request,
        'app/add_part.html',
        {
            "ErrorText":ErrorText,
            "SuccessText":SuccessText,
            'url':'/add_part/r',
            'Form':Form,
            'PartForm':PartAddSelectForm({'Part':'r'}),
            'title':'Add Part',
        })
