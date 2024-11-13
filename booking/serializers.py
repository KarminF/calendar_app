from rest_framework import serializers
from .models import DeviceInstance, DeviceBookingCalendar

class DeviceInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInstance
        fields = '__all__'

class DeviceBookingCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceBookingCalendar
        fields = '__all__'
