from django.contrib import admin

from .models import ProjectModel, ProjectPartModel, BOMDesignatorModel

# Register your models here.
class BOMDesignatorAdminInline(admin.TabularInline):
    model = BOMDesignatorModel

@admin.register(ProjectPartModel)
class ProjectPartModelAdmin(admin.ModelAdmin):
    inlines = [BOMDesignatorAdminInline,]

admin.site.register(ProjectModel)
admin.site.register(BOMDesignatorModel)
