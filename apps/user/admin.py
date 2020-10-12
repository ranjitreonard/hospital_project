from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (('Login'), {'fields': ('staff_id', 'username', 'password')}),
        (_('Personal_info'), {'fields': ('first_name', 'last_name', 'user_type', 'role')}),
        (_('Permission'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staff_id', 'password', 'password2')
        })
    ),

    list_display = ('staff_id', 'first_name', 'last_name', 'user_type', 'role')

    search_fields = ('staff_id', 'first_name', 'last_name')
    ordering = ('staff_id',)
