from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime

from invoiceapp.models import Invoice, InvoiceDetail
from invoiceapp.serializers import InvoiceSerializer, InvoiceDetailSerializer
# from django.

# Create your views here.
@csrf_exempt
def invoice(request):
    data = {}
    if request.method == "POST":
        request_data = JSONParser().parse(request)
        if not request_data['customerName']:
            data['message'] = "Customer Name Is Required"

        request_data['date'] = datetime.today().strftime("%Y-%m-%d")
        invoiceSerializerData =  InvoiceSerializer(data = request_data)

        if invoiceSerializerData.is_valid() :
            data_save = invoiceSerializerData.save()
            data['id'] = data_save.id
            data['message'] = "Invoice Save"
            return JsonResponse(data= data, safe= False)
        data['message'] = "Invoice Not Save"
        return JsonResponse(data= data, safe= False)
    data['message'] = "Invalid Request"
    return JsonResponse(data= data ,safe= False)