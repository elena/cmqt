import datetime, pytz
from django import forms
from django.contrib import admin

from models import MetaChoice,InvoiceMeta,InvoiceType,Invoice,InvoiceItem,InvoiceSent
from ledgers.banks.models import Paid

class MetaChoiceAdmin(admin.ModelAdmin):
    list_display = ('name','type')
    list_filter = ('type', )

admin.site.register(MetaChoice,MetaChoiceAdmin)
admin.site.register(InvoiceType,)

# -- Invoice -- #
'''
def make_date(modeladmin, request, queryset):
    queryset.update(date='2010-02-28')
make_date.short_description = "date whatever'"
'''

today = datetime.datetime.date(datetime.datetime.now(pytz.timezone('Australia/Sydney')))    
def mark_paid(modeladmin, request, queryset, date=today):
    for a in queryset:
        i = Paid(invoice=a, date=today)
        i.save()
mark_paid.short_description = "Mark as paid today: %s" % today


class MetaForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea(attrs={'rows':'1',}),required=False) #css attribute - can be any

    class Meta:
        model = InvoiceMeta

class MetaInline(admin.TabularInline):
    form = MetaForm
    model = InvoiceMeta
    extra=1

class ItemForm(forms.ModelForm):
    item = forms.CharField(widget=forms.Textarea(attrs={'rows':'2',}),required=False) #css attribute - can be any
    #nett = forms.CharField(widget=forms.TextInput(attrs={'size':'8',})) #css attribute - can be any
    #on hold til can work out how to make column title correct (rather than 'None', which is default)
    
class Meta:
        model = InvoiceItem

class ItemInline(admin.TabularInline):
    form = ItemForm
    model = InvoiceItem
    extra=1

class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ('ref','date', 'type', 'contact', 'inv', 'total')
    list_filter = ('type', 'contact')
    search_fields = ('ref',)
    #actions = [make_date]
    actions = [mark_paid]
    inlines = [MetaInline,ItemInline]

admin.site.register(Invoice, InvoiceAdmin)
# -- end Invoice -- #

admin.site.register(InvoiceMeta,)
admin.site.register(InvoiceItem,) #, InvoiceItemAdmin)
admin.site.register(InvoiceSent,) #, InvoiceItemAdmin)
