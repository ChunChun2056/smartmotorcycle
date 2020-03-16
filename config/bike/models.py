from django.db import models
from django.contrib.auth.models import User
from threadlocals.threadlocals import get_current_request
import uuid
# Create your models here.


class Customers(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer")
    
    def __str__(self):
        return str(self.user.username)

class Devices(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    user = models.ForeignKey(Customers, on_delete=models.CASCADE)

    registered_on = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Devices"
        verbose_name_plural = "Devices"

    def save(self, *args, **kwargs):
        if not self.created_by:
            request = get_current_request()
            self.created_by = request.user

        return super().save(*args, **kwargs)

    @property
    def device_id(self):
        return str(self.id)

    def __str__(self):
        return "Device '{}' owned by '{}'.".format(self.device_id, self.user.user.username)


class Location(models.Model):
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    device = models.ForeignKey(
        Devices, on_delete=models.CASCADE, related_name="location")

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Lon: {} | Lat: {} | Device: {} | Timestamp: {}".format(
            self.longitude,
            self.latitude,
            self.device,
            self.timestamp.strftime("%Y %b. %d %I:%M:%S %p")
        )

    @property
    def json_parsed(self):
        return {
            'lon':self.longitude,
            'lat':self.latitude,
            'timestamp':self.get_timestamp(),
        }

    @property
    def location(self):
        return "{}, {}".format(self.longitude, self.latitude)

    def get_timestamp(self):
        return self.timestamp.strftime("%Y %b. %d %I:%M:%S %p")
