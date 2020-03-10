from django.contrib import admin
from app.models import ShelfModel, ContainerModel, PackageModel
from app.models import PartCategoryModel, PartModel, PartAttrModel, PartCountModel

class PartCountModelAdminInline(admin.TabularInline):
    model = PartCountModel

class PartAttrAdminInline(admin.TabularInline):
    model = PartAttrModel
    min_num = 1

class PartModelAdmin(admin.ModelAdmin):
    inlines = [PartCountModelAdminInline,]


admin.site.register(ShelfModel)
admin.site.register(ContainerModel)
admin.site.register(PackageModel)
admin.site.register(PartCategoryModel)
admin.site.register(PartModel, PartModelAdmin)
admin.site.register(PartAttrModel)
admin.site.register(PartCountModel)
