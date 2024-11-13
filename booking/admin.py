from django.contrib import admin

# Register your models here.
from .models import DeviceInstance, DeviceBookingCalendar
register_models = [DeviceInstance, DeviceBookingCalendar]
admin.site.register(register_models)