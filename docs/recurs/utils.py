import datetime, pytz
from decimal import Decimal

from docs.recurs.models import MetaRecur, RecurType, Recur, RecurInstance
from docs.invoices.models import InvoiceType, Invoice, InvoiceMeta, InvoiceType, MetaChoice, InvoiceItem
from docs.models import ItemCss
from ledgers.account_metas.models import Interval

from docs.utils import make_template_url, make_inv_ref, get_inv_num, get_items, string_decimal


def create_recur_invoice(x, is_due, start, end): 
    today = is_due
    #today = datetime.datetime.date(datetime.datetime.now(pytz.timezone('Australia/Sydney')))
    it = InvoiceType.objects.get(name__icontains='webhost')
    re = x
    c = re.contact
    i = get_inv_num(c)
    # numbers
    a = re.amount
    j = int(re.interval.months)
    if re.interval.months==12:
        annual = True
        if re.annual:
            ja = re.annual
            a = Decimal(re.annual/12)
        else:
            ja = Decimal(j*a)
    else:
        annual = False
        ja = Decimal(j*a)       

    ga = string_decimal(ja*Decimal('0.1'))
    gs = '%s.%s' % (ga[0],ga[1])
    gst = Decimal(gs)

    ta = string_decimal(str(round(ja+gst,2)))
    total = '%s.%s' % (ta[0],ta[1])
    
    na = string_decimal(ja)
    ja = '%s.%s' % (na[0],na[1])
    
    
    # *invoice
    inv = Invoice(
        type    = it,
        date    = today,
        contact = c,
        inv     = i,
        ref     = make_inv_ref(c, i),
        nett    = ja,
        gst     = gst,
        total   = total
    )
    inv.save() 
    
    # *invoice metas
    inm = InvoiceMeta(
        invoice = inv,
        choice = MetaChoice.objects.get(name='box_hdr'),
        detail = 'Invoice for Ongoing Webhosting'
    )
    
    # *invoice items
    ra = string_decimal(ja)
    ea = string_decimal(a)           
    if annual:
        detail1 = '12 months web hosting @ $%s.%s (not including GST)' % (ra[0],ra[1])
    else:
        detail1 = 'Web hosting @ $%s.%s per month (not including GST)' % (ea[0],ea[1])
    ini1 = InvoiceItem(
        meta_id = 1,
        invoice = inv,
        order = 1,
        item = detail1,
        qty = j,
        each = '$ %s.%s' % (ea[0],ea[1]),
        nett = '$ %s.%s' % (ra[0],ra[1])
    )
    
    detail2 = '%s %s - %s %s' % (start.day, start.strftime('%B %Y'),end.day,end.strftime('%B %Y'))
    ini2 = InvoiceItem(
        meta_id = 1,
        invoice = inv,
        order = 2,
        item = detail2,
        css = ItemCss.objects.get(name='hosting_period')
    )
    
    ri = RecurInstance(
        cover_end = end.strftime('%Y-%m-%d'),
        cover_start = start.strftime('%Y-%m-%d'),
        invoice = inv,
        recur = x
    )   
    
    inm.save()
    ini1.save()
    ini2.save()
    ri.save()
    return inv