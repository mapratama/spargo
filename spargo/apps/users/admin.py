from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class UserAdmin(DjangoUserAdmin):
    #  for edit
    fieldsets = (
        (None, {'fields': ('email', 'name', 'mobile_number', 'password', 'photo',
                'gender', 'birthday', 'gcm_key', 'notification', 'last_sync_posts')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    # for add
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    list_display = ('email', 'name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('name', 'email')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
