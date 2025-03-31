from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from api.models import (
    UserTrackable,
    TimeStamped
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
   
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser not allowed to log in.'))
        
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, verbose_name=_('username'))
    name = models.CharField(max_length=150, verbose_name=_('name'))
    init_password = models.CharField(max_length=10, verbose_name=_('initial password'), null=True, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name=_('staff status'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_('date joined'))
    question = models.TextField(verbose_name=_('question'), null=True, blank=True)
    answer = models.TextField(verbose_name=_('answer'), null=True, blank=True)
    is_default_password = models.BooleanField(verbose_name=_('is default password?'), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class CustomUserPermission(UserTrackable, TimeStamped):
    access_level = models.CharField(max_length=20, verbose_name=_('access level'))
    can_read_eval_data = models.BooleanField(default=True, verbose_name=_('can read evaluation data'))
    can_write_eval_data = models.BooleanField(default=False, verbose_name=_('can write evaluation data'))
    can_read_eval_settings = models.BooleanField(default=False, verbose_name=_('can read evaluation settings'))
    can_write_eval_settings = models.BooleanField(default=False, verbose_name=_('can write evaluation settings'))
    can_read_criteria_settings = models.BooleanField(default=False, verbose_name=_('can read criteria settings'))
    can_write_criteria_settings = models.BooleanField(default=False, verbose_name=_('can write criteria settings'))
    can_export = models.BooleanField(default=False, verbose_name=_('can export'))

    def __str__(self):
        return f'{self.access_level}'   

class Team(UserTrackable, TimeStamped):
    parent_team = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('parent team'))
    name = models.CharField(max_length=200, verbose_name=_('name'))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))
    
    def __str__(self):
        return f'{self.name}'
    
class Employee(UserTrackable, TimeStamped):
    class RoleNameEnum(models.TextChoices):
        PM = 'Project Manager', 'PM'
        SM = 'Scrum Master', 'SM' 
        TL = 'Team Lead', 'TL'
        DEV = 'Developer', 'DEV'
        TEST = 'Tester', 'TEST' 

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('user'))
    access_level = models.ForeignKey(CustomUserPermission, on_delete=models.CASCADE, verbose_name=_('access level'))
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_('team'))
    role = models.CharField(max_length=150, choices=RoleNameEnum.choices, default=RoleNameEnum.DEV, verbose_name=_('role'))
    is_active = models.BooleanField(default=True, verbose_name=_('active status'))

    def __str__(self):
        return f'{self.user.username} - {self.team.name}'