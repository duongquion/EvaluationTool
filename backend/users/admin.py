from django.contrib import messages
from django.utils.timezone import now
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from .forms import (
    CustomUserCreationForm
)

from .models import (
    CustomUser,
    Team,
    CustomUserPermission,
    Employee,
)

from .containts import (
    AlertMessage,
)

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
        
class CustomUserPermissionAdmin(admin.ModelAdmin):
    model = CustomUserPermission
    list_display = (
        'access_level',
        'can_read_eval_data',
        'can_read_eval_settings',
        'can_read_criteria_settings',
        'can_export',
    )
    list_filter = (
        'access_level',
        'can_write_eval_data',
        'can_write_eval_settings',
        'can_write_criteria_settings',
    )
    search_fields = ('access_level',)
    ordering = ('id',)
 
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = (
        'user',
        'access_level',
        'team',
        'role',
        'is_active',
        'created_at',
        'updated_user',
    )
    list_filter = (
        'role',
        'team',
    )
    ordering = ('id', )
    
    def save_model(self, request, obj, form, change):
        if not change:
            last_employee = Employee.objects.filter(user=obj.user).order_by('-created_at').first()
            if last_employee:
                days_difference = now().month - last_employee.created_at.month
                print(days_difference)
                if days_difference < 3:
                    self.message_user(
                        request,
                        AlertMessage.UNSUCCESS_FOR_ADD_NEW_EMPLOYEE,
                        level=messages.ERROR
                    )
                    return
        super().save_model(request, obj, form, change)
 
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = (
        "name",
        "parent_team",
        "is_active",
        "updated_at",
        "updated_user",
    )
    list_filter = (
        "is_active",
    )
    ordering = ('id', )
        
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team, TeamAdmin )
admin.site.register(CustomUserPermission, CustomUserPermissionAdmin)
admin.site.register(Employee, EmployeeAdmin)