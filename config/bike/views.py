from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError   
from .models import Devices, Customers, Location
import json
# Create your views here.

@csrf_exempt
def authenticate_user(request, **kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')

    try:
        user = User.objects.get(username=username)
        status = user.check_password(password)
        if not status:
            raise Exception
    except:
        status = False

    return HttpResponse(json.dumps(status))

@csrf_exempt
def set_location(request, **kwargs):
    device_id = kwargs['pk']
    device = Devices.objects.get(pk=device_id)

    if request.method == "GET":
        lon = request.GET.get("lon")
        lat = request.GET.get("lat")
    elif request.method == "POST":
        lon = request.POST.get("lon")
        lat = request.POST.get("lat")
    else:
        return HttpResponseBadRequest

    location, created = Location.objects.get_or_create(
        device=device,
    )

    location.longitude=lon
    location.latitude=lat
    location.save()

    return JsonResponse(location.json_parsed)

@csrf_exempt
def device_location(request, **kwargs):
    device_id = kwargs['pk']

    device = Devices.objects.get(pk=device_id)

    device_locations = device.location.all()

    for location in device_locations:
        location_data = {
            'lon':location.longitude,
            'lat':location.latitude,
            'timestamp':location.get_timestamp(),
        }

    json_parsed_data = {
        'device':device.pk,
        'owner':device.user.user.username,
        'location':location_data
    }

    return JsonResponse(json_parsed_data)

class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "home.html"

class RegisterUser(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "registration/register_user.html"

    def post(self, *args, **kwargs):
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        username = self.request.POST.get("username")
        email = self.request.POST.get("email")
        password = self.request.POST.get("password")
        repassword = self.request.POST.get("repassword")

        if password != repassword:
            messages.error(self.request, "Password does not match.")
        else:
            try:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password,
                )

                Customers.objects.create(
                    user=user
                )
            except IntegrityError:
                messages.error(self.request, "This User Already Exists!")
            except Exception as e:
                print("Exception on 'RegisterView':", e)
                messages.error(self.request, "Something went wrong.")
            else:
                messages.success(self.request, "User Created!")
        
        return self.get(*args, **kwargs)

class AddDevice(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "registration/add_device.html"

    def post(self, *args, **kwargs):
        user = self.request.POST.get("user")

        try:
            user_obj = Customers.objects.get(pk=user) 
            Devices.objects.create(
                user=user_obj
            )

            messages.success(self.request, "Device Added.")
        except Exception as e:
            print("Exception on 'AddDevice':", e)
            messages.error(self.request, "Something went wrong.")
        
        return self.get(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["users"] = Customers.objects.all()
        return context

class DeviceListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "devices.html"
    model = Devices
    paginate_by = 50
    queryset = Devices.objects.all()
    context_object_name = 'devices'
