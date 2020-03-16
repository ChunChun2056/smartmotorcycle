from django.urls import path
from . import views
# from django.contrib.auth.views import login, logout

urlpatterns = [
    # path('login', login, name='login'),
    path('', views.HomeView.as_view(), name='home'),

    path('register-user', views.RegisterUser.as_view(), name='register-user'),
    path('add-device', views.AddDevice.as_view(), name='add-device'),
    path('devices', views.DeviceListView.as_view(), name='devices'),

    ### API
    path('location/<pk>', views.device_location, name='get-device-location'),
    path('set-location/<pk>', views.set_location, name='set-device-location'),
]
