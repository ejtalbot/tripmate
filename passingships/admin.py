from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

admin.site.unregister(User)
admin.site.register(User)
