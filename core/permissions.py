from rest_framework.permissions import BasePermission


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
