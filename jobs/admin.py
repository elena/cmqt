from django.db import models
from django.contrib import admin

from jobs.models import Job, JobStage


class StageInline(admin.TabularInline):
    model = JobStage
    extra=2


class JobAdmin(admin.ModelAdmin):
    list_display = ('name','contact','finished')
    inlines = [StageInline]

admin.site.register(Job,JobAdmin)  
    

class JobStageAdmin(admin.ModelAdmin):
    list_display = ('job','phase','detail','order','notes')
    list_filter = ('job','order')

admin.site.register(JobStage,JobStageAdmin)