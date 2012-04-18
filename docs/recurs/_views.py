import datetime, pytz

from docs.invoices.models import Invoice, InvoiceSent
from docs.recurs.models import MetaRecur, RecurType, Recur, RecurInstance
from docs.recurs.utils import create_recur_invoice


rt = RecurType.objects.filter(name__icontains='host')[0]
rs = RecurInstance.objects.all()
r = Recur.objects.filter(live=1, dd=0,type=rt)
today = datetime.datetime.date(datetime.datetime.now(pytz.timezone('Australia/Sydney')))

   
def find_next_start(x):
    t = datetime.timedelta(days=1)
    try:
        ro = rs.filter(recur=x).order_by('-cover_end')[0]
        next_start = ro.cover_end + t
    except:
        next_start = x.start 
    return next_start
    
def current_hosting(gen=False): 
    i = 0
    l = {}
    for x in r:
        next_due = find_next_start(x)
        m = MetaRecur.objects.get(name='check_within_days')
        d = datetime.timedelta(days=float(m.value))
        is_due = next_due-d
        try: 
            ro = rs.filter(recur=x).order_by('-cover_end')[0]
            end = ro.cover_end
        except: 
            end = x.start
        # TD: not convinced that the 2 things going on below shouldn't be seperated
        if is_due<today:
            if gen: # CREATE THE MAGIC
                start = end+datetime.timedelta(days=1)       
                end = next_due
                create_recur_invoice(x, is_due, start, end)
            else:
                l[x.client.name] = [x, 'invoiced up to/start: %s | next due: %s | check: %s' % (end, next_due, is_due)]
    return l


def create_recur(x):
    is_due = today
    t = datetime.timedelta(days=x.interval.days) # this recurs' interval
    start = find_next_start(x)
    end = start+t
    create_recur_invoice(x, is_due, start, end)
    return ''
    #return '%s  |start:%s  |end:%s' % ('', start, end)
    

def outstanding(request): 
    return ''
    

def upcoming(request): 
    return ''


def outstanding(request): 
    return ''


def special_hosting(c,it):
    # must return dictionary to update into 'context'
    
    # 1 find cover_end
    # 2 add interval
    # 3 if today is within meta days
    return ''
    
    