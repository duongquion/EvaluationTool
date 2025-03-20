from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from .models import (
    CustomUser,
)
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = (
        "username",
        "init_password",
        "is_staff",
        "is_active",
        "is_default_password",
        "date_joined",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    staff_add_fieldsets = (("Username", {"fields": ("username", "name")}),)
    staff_edit_fieldsets = (
        ("Username ( Ex: Tran Anh Vu - vuta)", {"fields": ("username", "name")} ),
        ("Password", {"fields": ("is_default_password",)}),
        ("Permission", {"fields": ("is_active",)}),
    )
    superuser_add_fieldsets = (
        ("Username ( Ex: Tran Anh Vu - vuta)", {"fields": ("username", "name")} ),
        ("Permission", {"fields": ("is_staff", "is_superuser", "groups")} ),
    )
    superuser_edit_fieldsets = (
        ("Username ( Ex: Tran Anh Vu - vuta)", {"fields": ("username", "name")} ),
        ("Password", {"fields": ("is_default_password",)}),
        ("Permission", {"fields": ("is_staff", "is_superuser", "is_active", "groups")} ),
    )
    search_fields = ("username",)
    ordering = ("username",)
 
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            if request.user.is_superuser:
                return self.superuser_add_fieldsets
            else:
                return self.staff_add_fieldsets
        else:
            if request.user.is_superuser:
                return self.superuser_edit_fieldsets
            else:
                return self.staff_edit_fieldsets
 
    def save_model(self, request, obj, form, change):
        if change:
            current_user = CustomUser.objects.get(pk=obj.id)
            if (
                current_user.is_default_password == False
                and obj.is_default_password == True
            ):
                password = get_random_string(10)
                obj.init_password = password
                obj.set_password(password)
 
        else:
            password = get_random_string(10)
            obj.init_password = password
            obj.set_password(password)
 
        super().save_model(request, obj, form, change)
 
        if not (obj.is_staff or obj.is_superuser):
            obj.groups.clear()
 
        obj.save()
        
admin.site.register(CustomUser, CustomUserAdmin)