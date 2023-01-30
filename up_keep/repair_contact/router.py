from repair_contact.viewsets import RepairView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', RepairView)
