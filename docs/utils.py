from clients.contacts.models import Contact, Client
from docs.invoices.models import Invoice, InvoiceType
#from docs.models import MetaItem, ItemChoice
from ledgers.account_metas.models import OurAddress
from docs.recurs.models import Recur, RecurInstance


def make_template_url(template):
    return 'docs/items/%s' % template

def make_inv_ref(c, inv_num):
    return '%s-%04d-%04d' % (c.client.code,c.client.number,inv_num)

def get_inv_num(c): # get latest invoice number
    g = Invoice.objects.filter(contact__client__pk=c.client.pk)
    if g.count(): # check that it isn't the first
        h = g.order_by('-inv')[0]
        i=h.inv+1
    else:
        i=1
    return i

def get_items(c,it=False):
    # 1 contact has had one before
    # 2 client has before
    # 3i anyone has
    # 3ii meta item ## TD
    if it:
        i = Invoice.objects.filter(type=it)
    else:
        i = Invoice.objects.all()
    
    try: # 1
        i = i.filter(contact=c).order_by('-inv')[0]
    except:
        try: # 2
            i = i.filter(contact__client__pk=c.client.pk).order_by('-inv')[0]
        except:
            try: # 3 ... TD: replace this with MetaItem
                i = i.order_by('-pk')[0]
            except: pass
    return i

def string_decimal(ja):
    ra = str(ja).split(".")
    try:
        if len(ra[1])==1:
            ra[1] = '%s0' % ra[1]
        if len(ra[1])>2:
            ra[1] = '%s' % ra[1][:1]
    except:
        ra.append('00')
    return ra        
