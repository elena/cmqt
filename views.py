import datetime, pytz

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context
from django.db.models import Sum

from django.contrib.auth.models import User
from ledgers.banks.models import Paid
from jobs.models import Job, JobStage
from docs.invoices.models import Invoice, InvoiceSent
from docs.recurs.models import Recur
from docs.recurs.views import current_hosting, create_recur
from clients.contacts.models import Contact

#@staff_member_required
def test(request):
    context = {}
    context['sess'] = request.session.__dict__
    context['object_list'] = Invoice.objects.all().order_by('?')[0]
    template = ['test.html']
    return render_to_response(template, context_instance=RequestContext(request, context))
    

@staff_member_required
def home(request):
    context = {}
    if request.POST:
        r = request.POST
        try:
            r['gen_all']
            current_hosting(gen=True)
            return HttpResponseRedirect('/')
        except: pass

        try:
            #context['next_due'] = r['gen_select']
            for p in r:
                if p.find("|")>0:
                    if p.split("|")[1] == 'gen_select':
                        try:
                            p = int(p.split("|")[0])
                            x = Recur.objects.get(pk=p)
                            create_recur(x)
                            return HttpResponseRedirect('/')
                        except: pass
                    if p.split("|")[1] == 'sent_select':
                        # put the create_sent function here
                        pass
        except: pass
        
        try: # Paid.save()
            if r['paid']:
                d = datetime.datetime.strptime(r['date'],'%d-%b-%Y')
                i = Invoice.objects.get(pk=r['pk'])
                p = Paid(invoice=i, date=d)
                p.save()
            context['request'] = r
            return HttpResponseRedirect('/')
        except: pass

        try: # Sent.save()
            if r['sent']:
                d = datetime.datetime.strptime(r['date'],'%d-%b-%Y')
                u = User.objects.get(pk=request.session['_auth_user_id'])
                i = Invoice.objects.get(pk=r['pk'])
                s = InvoiceSent(invoice=i, date=d, user=u)
                s.save()
                context['request'] = s
                return HttpResponseRedirect('/')
        except: pass

        try: # Stage.save()
            if r['stage']:
                j = Job.objects.get(pk=r['pk'])
                nj = JobStage(job=j, phase=r['phase'], detail=r['detail'], notes=r['desc'])
                nj.save()
                context['request'] = r
                return HttpResponseRedirect('/')
        except: pass        

        try: # New Job.save()
            if r['stage']:
                c = Contact.objects.get(pk=r['contact'])
                j = Job(contact=c, name=r['name'])
                j.save()
                context['request'] = r
                return HttpResponseRedirect('/')
        except: pass        

        try: # Done (toggle) Job.save()
            if r['done']:
                j = Job.objects.get(pk=r['job'])
                s = JobStage(pk=r['pk'], job=j, live=0)
                s.save()
                context['request'] = r
                return HttpResponseRedirect('/')
        except: pass        

        
    q = Invoice.objects.filter(paid__isnull=True).order_by('contact__client', 'date')
    context['oustanding'] = q.aggregate(Sum('total'))
    context['paid_list'] = q
    context['contact_list'] = Contact.objects.filter(live=True).order_by('-pk')
    context['job_list'] = Job.objects.filter(finished=0)
    context['job_short'] = JobStage.objects.all().order_by('detail')
    context['new_host'] = current_hosting(gen=False)
    today = datetime.datetime.date(datetime.datetime.now(pytz.timezone('Australia/Sydney')))
    context['today'] = today
    so = InvoiceSent.objects.all()
    io = Invoice.objects.filter(date__gte=today-datetime.timedelta(days=366)).exclude(invoicesent__in=so)
    context['object_list'] = io.order_by('ref')
    context['schawk'] = Invoice.objects.filter(contact__client__name__icontains='schawk').order_by('-inv')
    template = ['index.new.html']
    return render_to_response(template, context_instance=RequestContext(request, context))
    
