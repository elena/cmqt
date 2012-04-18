from django.contrib import admin
from models import Paid



class PaidAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'date']
    
    
admin.site.register(Paid,PaidAdmin)