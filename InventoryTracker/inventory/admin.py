from django.contrib import admin
from .models import ShelfModel, ContainerModel, PackageModel
from .models import PartCategoryModel, PartModel, PartAttrModel, PartCountModel
from .models import ProjectModel, ProjectPartModel, BOMDesignatorModel

class PartCountModelAdminInline(admin.TabularInline):
    model = PartCountModel

class PartAttrAdminInline(admin.TabularInline):
    model = PartAttrModel
    min_num = 1

class BOMDesignatorAdminInline(admin.TabularInline):
    model = BOMDesignatorModel

@admin.register(ProjectPartModel)
class ProjectPartModelAdmin(admin.ModelAdmin):
    inlines = [BOMDesignatorAdminInline,]

@admin.register(PartModel)
class PartModelAdmin(admin.ModelAdmin):
    inlines = [PartCountModelAdminInline,]

admin.site.register(ShelfModel)
admin.site.register(ContainerModel)
admin.site.register(PackageModel)
admin.site.register(PartCategoryModel)
admin.site.register(PartAttrModel)
admin.site.register(PartCountModel)

admin.site.register(ProjectModel)
admin.site.register(BOMDesignatorModel)
