"""
URL configuration for ticket_sales_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views import CityListView, UserRegistrationView, StadiumView, StadiumListView, HallListView, HallView, \
    PlaceListView, PlaceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/cities/', CityListView.as_view(), name='city_list'),
    path('api/stadiums/list/', StadiumListView.as_view(), name='stadium_list'),
    path('api/stadiums/', StadiumView.as_view(http_method_names=['post'])),
    path('api/stadiums/<int:id>', StadiumView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/halls/list/<int:stadium_id>', HallListView.as_view(), name='hall_list'),
    path('api/halls/', HallView.as_view(http_method_names=['post'])),
    path('api/halls/<int:id>', HallView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/places/list/<int:hall_id>', PlaceListView.as_view(), name='place_list'),
    path('api/places/', PlaceView.as_view(http_method_names=['post'])),
    path('api/places/<int:id>', PlaceView.as_view(http_method_names=['put', 'delete'])),
]
