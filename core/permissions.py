from rest_framework.permissions import BasePermission

from core.models import EventRequest

class CanAddStadium(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_stadium')


class CanChangeStadium(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_stadium')


class CanDeleteStadium(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_stadium')


class CanAddHall(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_hall')


class CanChangeHall(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_hall')


class CanDeleteHall(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_hall')


class CanAddPlace(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_place')


class CanChangePlace(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_place')


class CanDeletePlace(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_place')


class CanAddEvent(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_event')


class CanChangeEvent(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_event')


class CanDeleteEvent(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_event')


class CanAddEventRequest(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_eventrequest')


class CanChangeEventRequest(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_eventrequest')


class CanDeleteEventRequest(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_eventrequest')


class CanAddPhoto(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_photo')


class CanDeletePhoto(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_photo')


class CanAddVideo(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_video')


class CanDeleteVideo(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_video')


class CanAddPromotion(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_promotion')


class CanChangePromotion(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_promotion')


class CanDeletePromotion(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_promotion')


class CanAddPromotionEvent(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_promotionevent')


class CanDeletePromotionEvent(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_promotionevent')


class CanApproveEventRequest(BasePermission):
    def has_permission(self, request, view):
        try:
            event_request = EventRequest.objects.get(id=request.data['id'])
            stadium_admin = event_request.event.hall.stadium.user
            return request.user == stadium_admin or request.user.is_superuser
        except EventRequest.DoesNotExist:
            return False
