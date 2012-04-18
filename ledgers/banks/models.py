from django.db import models

from docs.invoices.models import Invoice

class Paid(models.Model):
    invoice = models.ForeignKey(Invoice, unique=True)
    date = models.DateField()
    
    
