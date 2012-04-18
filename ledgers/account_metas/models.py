from django.contrib import admin
from django.db import models


class Instruction(models.Model):
    name   = models.CharField(max_length=42,)
    detail = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

admin.site.register(Instruction,)


class OurAddress(models.Model):
    show = models.TextField()
    changed = models.DateField()

    class Meta:
        verbose_name_plural = "our addresses" 
        
    def __unicode__(self):
        return self.show

admin.site.register(OurAddress,)


class FinancialYear(models.Model):
    name = models.CharField(max_length=42)
    start = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return self.name

admin.site.register(FinancialYear,)


class Interval(models.Model):
    name = models.CharField(max_length=42)
    months = models.IntegerField(null=True, blank=True)
    days = models.FloatField(null=True, blank=True)
	
    def __unicode__(self):
        return self.name

class IntervalAdmin(admin.ModelAdmin):
	list_display = ('name','months','days')
	list_filter = ('name',)
		
admin.site.register(Interval, IntervalAdmin)
