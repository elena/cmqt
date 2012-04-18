from django.conf.urls.defaults import *

from views import new_inv, new_qte, doc_new, doc_view, doc_schawk, inv_sent #, new_recur

urlpatterns = patterns('',   
    url(r'^schawk/$', doc_schawk, name='doc_schawk'),
    url(r'^sent/$', inv_sent, name='inv_sent'),
    url(r'^(?P<slug>[-\w]+)/$', doc_view, name='doc_view'),
    #url(r'^test/(?P<slug>[-\w]+)/$', band_audio),
    #url(r'^type/(?P<artisttype>[-\w]+)/$', band_type, name = "band_type"),

)

