import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context


from clients.contacts.models import Contact, Client
from docs.invoices.models import Invoice, InvoiceType, InvoiceMeta, InvoiceSent
#from docs.models import MetaItem#, ItemChoice
from ledgers.account_metas.models import OurAddress, Instruction
from docs.recurs.models import Recur, RecurInstance

from forms import doc_publish
from utils import make_template_url, make_inv_ref, get_inv_num, get_items


# seperate function to pull out all of the 'Meta' for init of document
# these are predetermined by a human being


@staff_member_required
def inv_sent(request): 
    context={}
    if request.POST:
        r = request.POST
        
    sent = InvoiceSent.objects.all()
    context['today'] = datetime.datetime.now()
    context['object_list'] = Invoice.objects.exclude(pk__in=sent)
    template = ['docs/sent.html']
    return render_to_response(template, context_instance=RequestContext(request, context))



@staff_member_required
def new_inv(request): 
    '''
    type    
    date    
    contact 
    inv     
    ref     
    nett    
    gst     
    total   
    '''
    return ''


@staff_member_required
def new_qte(request):
    return ''

        
@staff_member_required
def doc_view(request, slug):
    context = {}
    if request.POST:
        r = request.POST
        #try:
        doc_publish(r,context)
        slug = '/doc/%s/' % context['invoice'].ref
        return HttpResponseRedirect(slug)


    i = Invoice.objects.get(ref=slug)
    m = InvoiceMeta.objects.filter(invoice=i)
    context['ouraddress']    = OurAddress.objects.all()[0]
    context['contact']       = i.contact
    context['items']        = i
    context['date']         = i.date
    context['reference']    = i.ref
    try: context['box_hdr'] = m.get(choice__name='box_hdr')
    except: pass
    try: context['po_aew']  = m.get(choice__name='po_aew')
    except: pass
    try: context['po_ct']   = m.get(choice__name='po_ct')
    except: pass
    context['success']       = True
    context['item_template'] = make_template_url(i.type.template)
    template = ['inv/invoice.html']
    return render_to_response(template, context_instance=RequestContext(request, context))


@staff_member_required
def doc_new(request):
    context={}
    context['ouraddress']       = OurAddress.objects.all()[0]
    context['instruction']      = Instruction.objects.get(name__contains="invoice creation")
    context['dtype']            = 'i'#r['dtype'].split("|")[0]
    if request.POST:
        r = request.POST
        try:
            a = r['select'] 
            c = Contact.objects.get(pk=r['contact'].split("|")[0])
            itpk = r['itype'].split("|")[0]
            it = InvoiceType.objects.get(pk=itpk)           
            i = get_items(c,it)
            m = InvoiceMeta.objects.filter(invoice=i)
            context['date']             = datetime.datetime.now()
            context['reference']        = make_inv_ref(c, get_inv_num(c))
            context['items']            = i
            context['inv_num']          = get_inv_num(c)
            context['itype']            = it
            try: context['box_hdr'] = m.get(choice__name='box_hdr')
            except: pass
            template = ['inv/invoice.html']
            context['contact'] = c
            #context['request'] = r       
        except: 
            a = r['reference'] 
            try: 
                #return doc_view(request, )
                slug = '/doc/%s/' % context['invoice'].ref       
                return HttpResponseRedirect(slug)
            except:
                doc_publish(r,context)
                #return doc_view(request, context['invoice'].ref)
                slug = '/doc/%s/' % context['invoice'].ref
                return HttpResponseRedirect(slug)

    else:
        context['contacts0'] = Contact.objects.filter(live=1).filter(client__pk=1).order_by('id')
        context['contacts'] = Contact.objects.filter(live=1).exclude(client__pk=1).order_by('client', 'name')
        context['types'] = InvoiceType.objects.all()
        context['clients'] = Client.objects.filter(live=1).order_by('name')
        template = ['inv/select.html']
    return render_to_response(template, context_instance=RequestContext(request, context))


@staff_member_required
def doc_schawk(request):
    context = {}
    c = Contact.objects.get(name__icontains='doreen')
    context['ouraddress']       = OurAddress.objects.all()[0]
    context['instruction']      = Instruction.objects.get(name__contains="invoice creation")
    context['dtype']            = 'i'#r['dtype'].split("|")[0]
    context['date']             = datetime.datetime.now()
    context['reference']        = make_inv_ref(c, get_inv_num(c))
    context['contact']          = c
    context['itype']            = InvoiceType.objects.get(name__icontains='3d')
    context['items']            = Invoice.objects.filter(contact=c).order_by('-inv')[0]
    
    if request.POST:
        r = request.POST
        try:
            i = Invoice.objects.get(ref=r['reference'])
            m = InvoiceMeta.objects.filter(invoice=i)
            context['items']        = i
            context['date']         = i.date
            context['reference']    = r['reference']
        except:
            doc_publish(r,context)
            i = context['invoice']
            m = InvoiceMeta.objects.filter(invoice=i)
            context['items']        = i
            context['date']         = i.date
            context['reference']    = i.ref
            try: context['po_aew']  = m.get(choice__name='po_aew')
            except: pass
            try: context['po_ct']   = m.get(choice__name='po_ct')
            except: pass
            context['success']      = Instruction.objects.get(name__contains="success")
        

    template = ['inv/schawk.html']
    return render_to_response(template, context_instance=RequestContext(request, context))


    
'''
def new_recur(request):
    context={}
    #if request.POST:
    i = Invoice.objects.get(ref='CAP-0300-0009')                        # !! FIX
    c = i.contact
    context['ouraddress']= OurAddress.objects.all()[0]
    context['date']      = datetime.datetime.now()
    context['reference'] = make_inv_ref(c, 10)                          # !! FIX
    context['contact']   = c #this is easier than re-dev template
    context['dtype']     = 'i'
    
    context['items']     = i
    context['item_template'] = make_template_url(i.type.template)       



    context['request']  = request
    template = ['doc.html']
    return render_to_response(template, context_instance=RequestContext(request, context))
'''
