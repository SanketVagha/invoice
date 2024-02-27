from django.db import models
from django.db.models import Model
# Create your models here.


class Invoice(Model):
    id = models.AutoField(primary_key= True)
    date =models.DateField()
    customerName = models.CharField(max_length = 200)

class InvoiceDetail(Model):
    id = models.AutoField(primary_key= True)
    invoiceId = models.ForeignKey( Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length = 500)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    price = models.FloatField()
