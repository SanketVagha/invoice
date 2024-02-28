from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
from .background import Background

from invoiceapp.models import Invoice, InvoiceDetail
from invoiceapp.serializers import InvoiceSerializer, InvoiceDetailSerializer
# from django.

# Create your views here.
@csrf_exempt
def setinvoice(request):
    data = {}
    if request.method == "POST":
        request_data = JSONParser().parse(request)
        if not 'customerName' in request_data or not request_data['customerName']:
            data['message'] = "Customer Name Is Required"

        request_data['date'] = datetime.today().strftime("%Y-%m-%d")
        invoiceSerializerData =  InvoiceSerializer(data = request_data)

        if invoiceSerializerData.is_valid() :
            data_save = invoiceSerializerData.save()
            data['id'] = data_save.id
            data['message'] = "Record Save"
            return JsonResponse(data= data, safe= False)
        data['message'] = "Record Not Save"
        return JsonResponse(data= data, safe= False)
    data['message'] = "Invalid Request"
    return JsonResponse(data= data ,safe= False)

@csrf_exempt
def getinvoice(request):
    data = {}
    if request.method == "GET":
        getData = Invoice.objects.all()
        # print(getData.values())
        data['data'] = Background.querySet_to_dict(getData.values())
        # print(data)
        data['message'] = "Display the Data"
        return JsonResponse(data= data, safe= False)
    data['message'] = "Invalid Method"
    return JsonResponse(data= data, safe= False)

@csrf_exempt
def setinvoiceDetails(request):
    data = {}

    # Insert and Update The Invoice Details Data 

    if request.method == "POST":
        request_data = JSONParser().parse(request)
        
        if not 'invoiceId' in request_data or not request_data['invoiceId']:
            data['message'] = "Invoice Id Required"
            return JsonResponse(data= data, safe= False)

        invoiceId = Invoice.objects.only('id').filter(id = request_data['invoiceId']).count()
        
        if invoiceId == 0:
            data['message'] = "Invalid Id"
            return JsonResponse(data= data, safe= False)
        
        if not 'description' in request_data or not request_data['description']: 
            data['message'] = "Description Is Required"
            return JsonResponse(data= data, safe= False)
        
        if not 'quantity' in request_data or not request_data['quantity'] : 
            data['message'] = "Quantity Is Required"
            return JsonResponse(data= data, safe= False)
        
        if request_data['quantity'] <= 0:
            data['message'] = "Invalid Quantity"
            return JsonResponse(data= data, safe= False)
        
        if not 'unit_price' in request_data or not request_data['unit_price'] : 
            data['message'] = "Unit Price Is Required"
            return JsonResponse(data= data, safe= False)
        
        if request_data['unit_price'] <= 0 :
            data['message'] = "Invalid Unit Price"
        
        request_data['price'] = request_data['quantity'] * request_data['unit_price']

        if 'id' in request_data:
            invoiceDetailId = InvoiceDetail.objects.only('id').filter(id = request_data['id']).count()
            if invoiceDetailId == 0:
                data['message'] = "Invalid Id"
                return JsonResponse(data= data, safe= False)
            invoice_instance = InvoiceDetail.objects.get(pk=request_data['id'])
            invoiceDetailSerializerData = InvoiceDetailSerializer(invoice_instance, data = request_data, partial=True)

        else:    
            invoiceDetailSerializerData = InvoiceDetailSerializer(data = request_data)

        if invoiceDetailSerializerData.is_valid():
            data_save = invoiceDetailSerializerData.save()
            data['id'] = data_save.id
            data['message'] = "Data Save"
            return JsonResponse(data= data, safe= False)
        data['message'] = "Data Not Save"
        return JsonResponse(data= data, safe= False)
    
    #  Delete The Invoice Detele Deta

    if request.method == "DELETE":
        request_data = JSONParser().parse(request)
        
        if not 'id' in request_data or not request_data['id'] :
            data['message'] = "Id Required"
            return JsonResponse(data= data, safe= False)
        
        invoiceDetailId = InvoiceDetail.objects.only('id').filter(id = request_data['id']).count()

        # print(invoiceDetailId)
        if invoiceDetailId == 0:
            data['message'] = "Invalid Id"
            return JsonResponse(data= data, safe= False)
        
        invoiceDetailId = InvoiceDetail.objects.get(id=request_data['id'])
        id = invoiceDetailId.delete()
        if id:
            data['id'] = request_data['id']
            data['message'] = "Invoice Delete Successfully"
            return JsonResponse(data= data, safe= False)
        data['id'] = request_data['id']
        data['message'] = "Invoice Delete Fail"
        return JsonResponse(data= data, safe= False)
        
    data['message'] = "Invalid Request"
    return JsonResponse(data= data, safe= False)



@csrf_exempt
def getinvoiceDetails(request):
    data = {}
    if request.method == "GET":
        request_data = JSONParser().parse(request)

        if not 'id' in request_data or not request_data['id'] :
            data['message'] = "Id Required"
            return JsonResponse(data= data, safe= False)
        
        invoiceDetailId = InvoiceDetail.objects.only('id').filter(id = request_data['id']).count()
        # print(invoiceDetailId)
        if invoiceDetailId == 0:
            data['message'] = "Invalid Id"
            return JsonResponse(data= data, safe= False)
        
        getData = InvoiceDetail.objects.filter(id = request_data['id'])
        data['data'] = Background.querySet_to_dict(getData.values())
        data['message'] = "Display the Data"
        return JsonResponse(data= data, safe= False)
    data['message'] = "Invalid Request"
    return JsonResponse(data= data, safe= False)


@csrf_exempt
def getCustomerInvoiceDetails(request):
    data = {}
    if request.method == "GET":
        request_data = JSONParser().parse(request)
        if not 'id' in request_data or not request_data['id']:
            data['message'] = "Id Required"
            return JsonResponse(data= data, safe= False)
        
        invoiceDetailId = Invoice.objects.filter(id = request_data['id']).count()
        # print(invoiceDetailId)
        if invoiceDetailId == 0:
            data['message'] = "Invalid Id"
            return JsonResponse(data= data, safe= False)

        # getData = InvoiceDetail.objects.filter(invoiceId= request_data['id']).select_related('Invoice')

        getData = InvoiceDetail.objects.select_related('invoiceId').filter(invoiceId = request_data['id'])
        

        data['data'] =  Background.querySet_to_dict(getData.values())
        for details in getData:
            data['customerName'] =  details.invoiceId.customerName
            data['date'] = details.invoiceId.date
            break
        data['message'] = "Display the Data"
        return JsonResponse(data= data, safe= False)
    data['message'] = "Invalid Method"
    return JsonResponse(data= data, safe= False)
