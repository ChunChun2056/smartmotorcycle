from django.contrib import admin
from . import models
# Register your models here.

class LocationAdmin(admin.ModelAdmin):
    model = models.Location

    list_display = [
        'longitude',
        'latitude',
        'device',
        'timestamp'
    ]

class DeviceAdmin(admin.ModelAdmin):
    model = models.Devices

    list_display = [
        'device_id',
        'user'
    ]

    def device_id(self, obj):
        return obj.id


admin.site.register(models.Devices, DeviceAdmin)
admin.site.register(models.Location, LocationAdmin)
