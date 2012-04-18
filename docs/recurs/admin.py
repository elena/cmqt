from django.contrib import admin

from docs.recurs.models import MetaRecur, RecurType, Recur, RecurInstance


class MetaRecurAdmin(admin.ModelAdmin):
    list_display = ('name','value')
    list_filter  = ('name',) # just did this so it'll appear nicer in admin
    
admin.site.register(MetaRecur,MetaRecurAdmin)

admin.site.register(RecurType,)


class RecurAdmin(admin.ModelAdmin):
    list_display = ('client','type','interval','start','live', 'dd','amount')
    list_filter  = ('type','interval','client','dd')
    search_fields = ('client','type','interval','dd')

admin.site.register(Recur,RecurAdmin)


class RecurInstAdmin(admin.ModelAdmin):
    list_display = ('recur','cover_start','cover_end')
    list_filter  = ('recur','cover_start','cover_end')
    search_fields = ('recur','invoice','cover_start','cover_end')

admin.site.register(RecurInstance,RecurInstAdmin)


