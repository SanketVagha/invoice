
from django.urls import path
from invoiceapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('invoice', views.invoice, name="invoice")
]
