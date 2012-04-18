from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from views import home, test
from docs.views import new_inv, new_qte, doc_new, doc_view #, new_recur

urlpatterns = patterns('',
    url(r'^$', home, name = "home"),
    url(r'^test/', test, name = "test"),
    
    url(r'^new/invoice', new_inv, name = "new_inv"),
    url(r'^new/quote', new_qte, name = "new_qte"),
    url(r'^new/doc', doc_new, name = "doc_new"),

    (r'^doc/', include('docs.urls')),

    (r'^admin/$', 'indices.views.custom_admin_index'),  
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)


if settings.STATIC_SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
	)
else:
    pass