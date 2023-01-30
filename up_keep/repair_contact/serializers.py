from rest_framework import serializers
from repair_contact.models import RepairContact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairContact
        fields = ['id', 'name', 'email', 'contact_no', 'type_of_repairs']