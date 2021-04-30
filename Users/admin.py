from django.contrib import admin
from .models import Profile, Friends
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class FriendsAdmin(admin.ModelAdmin):
    list_display = (['UID', 'FID'])


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileInline]


admin.site.register(Friends, FriendsAdmin)
# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)


# class ProfileAdmin(admin.ModelAdmin):
# list_display = (['userName', 'birth_date', "profileImg", "gender"])
# search_fields = ['userName']
# inlines = [UserInline]
# Register your models here.

# admin.site.register(Profile, ProfileAdmin)
