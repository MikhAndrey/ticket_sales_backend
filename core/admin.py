from django.contrib import admin

from core.models import City, UserGroupRequest, User

admin.site.register(City)
admin.site.register(UserGroupRequest)
admin.site.register(User)
