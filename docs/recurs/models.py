'''
Invoices that are required to self-regenerate on a regular predicable basis.

- invoice
- automatically 
- regular
- predictable
'''

from django.db import models
from django.contrib import admin

from clients.contacts.models import Contact, Client, Domain
from docs.invoices.models import Invoice
from ledgers.account_metas.models import Interval


class MetaRecur(models.Model):
    ''' Malleable variables for use in application. Strictly specified at developement time. 
    
    DO NOT CHANGE 'name'. If the name is changed the recur application will PROBABLY BREAK.

    In general usage can be changed, but adding to these makes no sense and has no effect.
    '''
    name = models.CharField(max_length=42, )
    value = models.CharField(max_length=42, )
    
    def __unicode__(self):
        return self.name


class RecurType(models.Model):
    name = models.CharField(max_length=42, )
    
    def __unicode__(self):
        return self.name


class Recur(models.Model):
    ''' Every recurrance has their own recur. '''
    live    = models.BooleanField(default=1,)
    client  = models.ForeignKey(Client,) # these two serve diff purposes
    contact = models.ForeignKey(Contact,)      # contact for auto-generated address, client for forever assoc
    type    = models.ForeignKey(RecurType,)
    interval= models.ForeignKey(Interval,)
    domain  = models.ForeignKey(Domain, null=True, blank=True)
    amount  = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='amount monthly',
                help_text='Please put in a monthly amount if NOT annual, otherwise this will break regular invoice generation.')
    annual  = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='amount annually',
                help_text='Only used if annually recurring payment, then this amount will be used first and the monthly not used. If not annual this is ignored.')
    start   = models.DateField(null=True, blank=True, help_text='** go live **')
    dd      = models.BooleanField(default=0, verbose_name='direct deposit')

    def __unicode__(self):
        if self.type == 'domain':
            return self.domain
        else:
            return '%s - %s' % (self.client.code, self.interval)


class RecurInstance(models.Model):
    recur   = models.ForeignKey(Recur,)
    #contact = models.ForeignKey(Contact,) this field is superfluous ... should get it from inv
    invoice = models.ForeignKey(Invoice,)
    cover_start = models.DateField()
    cover_end   = models.DateField()
    
    def __unicode__(self):
        return '%s %s' % (self.recur, self.cover_start)

