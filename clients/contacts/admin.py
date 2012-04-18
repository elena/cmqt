from django.contrib import admin
from models import Client, Address, Contact, Domain


class OrganisationAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('name', 'number', 'code', 'invoice_name')
    prepopulated_fields = {"slug": ("name",)}


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('name', 'client')
    list_filter = ('client', 'live')
    prepopulated_fields = {"slug": ("name",)}

    
admin.site.register(Client, OrganisationAdmin)
admin.site.register(Address,)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Domain,)
