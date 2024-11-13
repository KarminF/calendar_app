from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceInstanceViewSet, DeviceBookingCalendarViewSet

router = DefaultRouter()
router.register(r'devices', DeviceInstanceViewSet)
router.register(r'bookings', DeviceBookingCalendarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
