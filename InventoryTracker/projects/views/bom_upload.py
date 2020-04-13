import csv
import chardet
from io import StringIO, TextIOWrapper

from django.views.generic.base import TemplateView
from django.http import HttpRequest, HttpResponse

from projects.forms import BOMUploadSelectForm

class BomUpload(TemplateView):
    """
    Allows upload a CSV based BOM list
    """
    template_name = "projects/bom_upload.html"

    def __init__(self, **kwargs):
        self.__Form = BOMUploadSelectForm()
        super().__init__(**kwargs)

    def post(self, request: HttpRequest, **kwargs)->HttpResponse:
        self.__Form = BOMUploadSelectForm(request.POST, request.FILES)
        if self.__Form.is_valid():
            F = self.__Form.cleaned_data['BOMFile']
            detector = chardet.UniversalDetector()
            for line in F.readlines():
                detector.feed(line)
                if detector.done: break

            detector.close()
            CSVFile = TextIOWrapper(F, encoding=detector.result['encoding'], errors='strict' )
            CSVFile.seek(0)
            Reader = csv.reader(CSVFile)
            self.__Headers = next(Reader)
            self.__Data = list(Reader)

        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BOM Upload"
        context['form'] = self.__Form
        context['headers'] = self.__Headers
        context['data'] = self.__Data
        return context
