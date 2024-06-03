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
    PlaceListView, PlaceView, EventView, PromotionView, FeedbackView, FeedbackListView, PromotionEventView, \
    EventPhotoView, EventPhotoListView, StadiumPhotoView, EventVideoListView, EventVideoView, UserListView, \
    EventRequestView, EventRequestPlaceView, EventRequestPlaceListView, EventPlaceListView, EventRequestUserListView, \
    EventRequestStadiumListView, PurchaseView, PurchaseCartView, PurchaseHistoryView
from messenger.views import ChatMessageView, ChatMessageListView, ChatListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/users/', UserListView.as_view(), name='user_list'),
    path('api/cities/', CityListView.as_view(), name='city_list'),
    path('api/stadiums/list/', StadiumListView.as_view(), name='stadium_list'),
    path('api/stadiums/', StadiumView.as_view(http_method_names=['post'])),
    path('api/stadiums/<int:id>', StadiumView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/stadiums/photos/', StadiumPhotoView.as_view(http_method_names=['post'])),
    path('api/stadiums/photos/<int:stadium_id>', StadiumPhotoView.as_view(http_method_names=['delete'])),
    path('api/halls/list/<int:stadium_id>', HallListView.as_view(), name='hall_list'),
    path('api/halls/', HallView.as_view(http_method_names=['post'])),
    path('api/halls/<int:id>', HallView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/places/list/<int:hall_id>', PlaceListView.as_view(), name='place_list'),
    path('api/places/', PlaceView.as_view(http_method_names=['post', 'put', 'delete'])),
    path('api/events/', EventView.as_view(http_method_names=['post'])),
    path('api/events/<int:id>', EventView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/events/photos/list/<int:event_id>', EventPhotoListView.as_view(http_method_names=['get'])),
    path('api/events/photos/', EventPhotoView.as_view(http_method_names=['post'])),
    path('api/events/photos/<int:id>', EventPhotoView.as_view(http_method_names=['delete'])),
    path('api/events/videos/list/<int:event_id>', EventVideoListView.as_view(http_method_names=['get'])),
    path('api/events/videos/', EventVideoView.as_view(http_method_names=['post'])),
    path('api/events/videos/<int:id>', EventVideoView.as_view(http_method_names=['delete'])),
    path('api/events/places/list/<int:event_id>', EventPlaceListView.as_view(http_method_names=['get'])),
    path('api/event-requests/', EventRequestView.as_view(http_method_names=['post', 'put'])),
    path('api/event-requests/<int:id>', EventRequestView.as_view(http_method_names=['delete'])),
    path('api/event-requests/list/', EventRequestUserListView.as_view(http_method_names=['get'])),
    path('api/event-requests/stadium-admin/list/', EventRequestStadiumListView.as_view(http_method_names=['get'])),
    path('api/event-requests/places/', EventRequestPlaceView.as_view(http_method_names=['post', 'delete'])),
    path('api/event-requests/places/list/<int:event_request_id>', EventRequestPlaceListView.as_view(http_method_names=['get'])),
    path('api/promotions/', PromotionView.as_view(http_method_names=['post'])),
    path('api/promotions/<int:id>', PromotionView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('api/feedbacks/list/<int:event_id>', FeedbackListView.as_view(http_method_names=['get'])),
    path('api/feedbacks/', FeedbackView.as_view(http_method_names=['post'])),
    path('api/feedbacks/<int:id>', FeedbackView.as_view(http_method_names=['put', 'delete'])),
    path('api/purchase/', PurchaseView.as_view(http_method_names=['post', 'put'])),
    path('api/purchase/<int:id>', PurchaseView.as_view(http_method_names=['delete'])),
    path('api/purchase/cart/', PurchaseCartView.as_view(http_method_names=['get'])),
    path('api/purchase/history/', PurchaseHistoryView.as_view(http_method_names=['get'])),
    path('api/promotion-events/', PromotionEventView.as_view(http_method_names=['post', 'delete'])),
    path('api/chats/', ChatListView.as_view(http_method_names=['get'])),
    path('api/messages/', ChatMessageView.as_view(http_method_names=['post'])),
    path('api/messages/<int:id>', ChatMessageView.as_view(http_method_names=['put', 'delete'])),
    path('api/messages/list/<int:chat_id>', ChatMessageListView.as_view(http_method_names=['get'])),
]
