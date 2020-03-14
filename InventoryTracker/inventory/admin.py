from django.contrib import admin
from .models import ShelfModel, ContainerModel, PackageModel
from .models import PartCategoryModel, PartModel, PartAttrModel, PartCountModel

class PartCountModelAdminInline(admin.TabularInline):
    model = PartCountModel

class PartAttrAdminInline(admin.TabularInline):
    model = PartAttrModel
    min_num = 1

@admin.register(PartModel)
class PartModelAdmin(admin.ModelAdmin):
    inlines = [PartCountModelAdminInline,]

admin.site.register(ShelfModel)
admin.site.register(ContainerModel)
admin.site.register(PackageModel)
admin.site.register(PartCategoryModel)
admin.site.register(PartAttrModel)
admin.site.register(PartCountModel)

