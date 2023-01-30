from rest_framework import viewsets
from . import serializers
from . import models
# Create your views here.


class RepairView(viewsets.ModelViewSet):
    queryset = models.RepairContact.objects.all()
    serializer_class = serializers.ContactSerializer




