
from django.urls import path
from invoiceapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('setinvoice', views.setinvoice, name="setinvoice"),
    path('getinvoice', views.getinvoice, name= "getinvoice"),
    path('setinvoiceDetails', views.setinvoiceDetails, name= "setinvoiceDetails"),
    path('getinvoiceDetails', views.getinvoiceDetails, name= "getinvoiceDetails"),
    path('getCustomerInvoiceDetails', views.getCustomerInvoiceDetails, name="getCustomerInvoiceDetails")
]
