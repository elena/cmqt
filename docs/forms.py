import re, string, datetime
from decimal import Decimal

from invoices.models import MetaChoice,InvoiceMeta,InvoiceType,Invoice,InvoiceItem
from docs.models import MetaItem
from clients.contacts.models import Contact

# FORM PROCESSING

def save_invoice(r):
    date = datetime.datetime.strptime(r['date'],'%d-%b-%Y')
    try: 
        inv_num = int(r['reference'].split("-")[-1])
    except: 
        inv_num = r['inv_num']


    i = Invoice(                        # Invoice
        type	= InvoiceType.objects.get(pk=3),#r['itype']),
        date	= date, #r['date'],
        contact	= Contact.objects.get(pk=r['contact_id']),
        inv	    = inv_num, #re.sub(r'[^0-9.]','',inv_num),
        ref	    = r['reference'],
        nett	= str(re.sub(r'[^0-9.]','',r['inv_nett'])),
        gst	    = str(re.sub(r'[^0-9.]','',r['inv_gst'])),
        total	= str(re.sub(r'[^0-9.]','',r['inv_total']))
    )

    try: 
        ipk = Invoice.objects.get(ref=r['reference'])
        i.pk = ipk.pk
    except: pass

    i.save()
    return i
    

def add_invoice_metas(r,i):
    l = []
    for k,v in r.iteritems():
        m = MetaChoice.objects.all()
        if m.filter(name__exact=k):     # InvoiceMeta
            m = m.filter(name__exact=k)[0]
            if v!='':
                l = InvoiceMeta(invoice=i, choice=m, detail=v)
                l.save()
    return l


def add_invoice_items(r,i):
    d = {}
    # create dict of items
    for k,v in r.iteritems():
        if re.match('^\d',k):           # InvoiceItem  
            new_k = int(k.split('|')[0])
            new_dict_items = {k: v}
            if not d.has_key(new_k): 
                d[new_k] = {'item_total':'','item_p':'','item_qty':'','item_each':'','item_total':'','item_gst':'','item':''}
            d[new_k][k.split('|')[1]]=v

    for z,x in d.iteritems():
        t = ''
        t = InvoiceItem(
            invoice	= i,
            order	= z,
            meta    = MetaItem.objects.get(pk=1)
        )
        try: t.title = x['item_h2']
        except: pass
        try: t.item  = x['item_p']
        except: pass 
        try: t.qty   = x['item_qty']
        except: pass 
        try: t.each  = x['item_each']
        except: pass 
        try: t.nett  = x['item_total']
        except: pass 
        try: t.gst   = x['item_gst']
        except: pass 
        try: t.total = x['item']
        except: pass 
        t.save()
    return t
        
        
def doc_publish(r, context):
    i = save_invoice(r)
    l = add_invoice_metas(r,i)
    t = add_invoice_items(r,i)
    
    context['invoice'] = i              # Invoice
    context['invmeta'] = l              # InvoiceMeta
    context['invitem'] = t              # InvoiceItem
    return context
