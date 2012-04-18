#from docs.invoices.models import Invoice

from django.contrib import admin
from django.db import models


class ItemCss(models.Model):
    name = models.CharField(max_length=42,
        help_text = "CSS id/class must exist in template."
    )

    class Meta:
        db_table = 'items_itemcss'
        verbose_name = "Item css"
        verbose_name_plural = "Item css"
    
    def __unicode__(self):
        return self.name

admin.site.register(ItemCss,)
  

class MetaItem(models.Model):
    ref = models.CharField(max_length=42,
        help_text = "For reference only."
    )
    title   = models.CharField(max_length=256,null=True, blank=True)
    item    = models.TextField(null=True, blank=True)
    css     = models.ForeignKey(ItemCss, null=True, blank=True)
    order   = models.IntegerField()
    qty     = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    each    = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    nett    = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    gst     = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    total   = models.CharField(max_length=256, null=True, blank=True)
    
    class Meta:
        db_table = 'items_metaitem'
        ordering = ['order']

    def __unicode__(self):
        return self.ref

admin.site.register(MetaItem,)

'''
class ItemChoice(models.Model):
    ref     = models.CharField(max_length=42,null=True, blank=True)
    #meta    = models.ForeignKey(MetaItem,)
    #type    = models.ForeignKey(InvoiceType,)
    title   = models.CharField(max_length=256,null=True, blank=True)
    css     = models.ForeignKey(ItemCss, null=True, blank=True)
    item    = models.TextField(null=True, blank=True)
    order   = models.IntegerField()
    qty     = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    each    = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    nett    = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    gst     = models.CharField(max_length=256, null=True, blank=True) #cheaper to keep copy here
    total   = models.CharField(max_length=256, null=True, blank=True)
    
    def __unicode__(self):
        return self.ref

admin.site.register(ItemChoice,)
'''