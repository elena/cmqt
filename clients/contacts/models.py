from django.contrib import admin
from django.db import models


class Address(models.Model):
    address_left = models.TextField(null=True,blank=True)
    address_right = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "addresses" 
        db_table = 'contact_address'       


class Client(models.Model):
    live = models.BooleanField(default=1,)
    name = models.CharField(max_length=30, help_text="name for general reference")
    invoice_name = models.CharField(max_length=240, null=True, blank=True, 
        help_text="name for the invoice to be made out to", verbose_name="name to go on invoice")
    slug = models.SlugField(max_length=42,)
    number = models.IntegerField()
    code = models.CharField(max_length=3,)
    #address = models.ForeignKey(Address,)
    address_left = models.TextField(null=True,blank=True)
    address_right = models.TextField(null=True,blank=True)
    
    class Meta:
        db_table = 'contacts_organisation'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    live = models.BooleanField(default=1,)
    client = models.ForeignKey(Client,)
    name = models.CharField(max_length=240,)
    slug = models.SlugField(max_length=42,)
    #address = models.ForeignKey(Address,)
    address_left = models.TextField(null=True,blank=True)
    address_right = models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return '%s -- %s' % (self.name, self.client)

    class Meta:
        ordering = ['name']


class Domain(models.Model):
    contact = models.ForeignKey(Client,)
    domain  = models.CharField(max_length=255,)
    registrar_url   = models.CharField(max_length=255,help_text="The URL of the registrar. Using this URL should take us to where the domain can be managed.")
    domain_details  = models.TextField(null=True, blank=True, help_text="It would be helpful to but the login and password details to manage the domain with here.")
    
    def __unicode__(self):
        return self.domain

