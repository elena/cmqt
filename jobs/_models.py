from django.db import models
from django.contrib import admin

from clients.contacts.models import Contact

class Job(models.Model):
    name = models.CharField(max_length=42)
    contact = models.ForeignKey(Contact)
    finished = models.BooleanField(default=False,)
    
    def __unicode__(self):
        return self.name
    
    
class JobStage(models.Model):
    PHASE_CHOICES = (
        ('1', 'Early'),
        ('2', 'Main'),
        ('3', 'Finish'),
    )

    job = models.ForeignKey(Job,)
    date = models.DateField(auto_now=True,)
    phase = models.CharField(max_length=1, choices=PHASE_CHOICES)
    order = models.IntegerField(blank=True, null=True)
    detail = models.CharField(max_length=255,blank=True, null=True,) # this maybe a standard set in the future.
    notes = models.CharField(max_length=255,blank=True, null=True,)
    
    class Meta:
        ordering = ['order', 'id']