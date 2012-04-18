from django.db import models

from django.contrib.auth.models import User

from clients.contacts.models import Contact
from docs.models import ItemCss, MetaItem
#from ledgers.accounts_metas.models import FinancialYear


class InvoiceType(models.Model):
    name = models.CharField(max_length=42)
    template = models.CharField(max_length=128,help_text="Should end in '.html' or '.htm'")

    def __unicode__(self):
        return self.name


        

class MetaChoice(models.Model):
    '''
    This is completely pretermined in the css. These will only work if have been included in the template first.

    TD: a lot of hardcoding here - could be tidied.
    TD: internal debate about whether should be seperate MetaItem class. At the moment it's seperated out.   
    '''
    DOC_CHOICES = (('a', 'All'),('i', 'Invoice'),('q', 'Quote'))

    live    = models.BooleanField(default=1,)
    name    = models.CharField(max_length=42,help_text = "CSS/class must exist in template. This field represente the classes available. These all correspond to a fixed position!")
    type    = models.CharField(max_length=1, choices=DOC_CHOICES, null=True, blank=True, help_text = "This will make this field special and always generate with the first view. eg Quote disclaimer text, Invoice bank details.")
    detail  = models.TextField(null=True, blank=True,help_text = "Example contents.")
    date    = models.DateField(auto_now_add=True,)
    
    def __unicode__(self):
        try:
            return 's% (%s)'(self.name, self.type)
        except: return self.name


class Invoice(models.Model):
    type    = models.ForeignKey(InvoiceType,)
    date    = models.DateField()
    contact = models.ForeignKey(Contact,)
    inv     = models.IntegerField(max_length=10)
    ref     = models.CharField(max_length=42)          #cheaper to keep copy here
    nett    = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True) #cheaper to keep copy here
    gst     = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True) #cheaper to keep copy here
    total   = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)


    def __unicode__(self):
        return self.ref


class InvoiceMeta(models.Model):
    live    = models.BooleanField(default=1,)
    invoice = models.ForeignKey(Invoice,)
    choice  = models.ForeignKey(MetaChoice,)
    detail  = models.TextField()
    date    = models.DateField(auto_now_add=True,)
    

    def __unicode__(self):
        return self.choice.name

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice)
    meta    = models.ForeignKey(MetaItem)
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
        ordering = ['order']


class InvoiceSent(models.Model):
    invoice = models.ForeignKey(Invoice,)
    user    = models.ForeignKey(User,)
    date    = models.DateField()
    note    = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.invoice.ref, self.user)
