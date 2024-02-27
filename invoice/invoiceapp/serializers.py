from rest_framework import serializers
from invoiceapp.models import Invoice, InvoiceDetail

class InvoiceSerializer(serializers.ModelSerializer):
    # customer_id = serializers.ReadOnlyField()
    class Meta:
        model = Invoice
        fields = "__all__"
    
class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = "__all__"