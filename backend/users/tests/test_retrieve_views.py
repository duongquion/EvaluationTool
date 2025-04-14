from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from ..models import (
    CustomUser as User,
    Team,
    Employee,
    CustomUserPermission as Permission
)

class RetrieveTeamTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(
            username='OnDQ',
            password='@Abcde12345',
        )
        self.user.is_default_password = False
        self.user.save()
        
        self.perm_DEV = Permission.objects.create(
            access_level='DEV',
            can_read_eval_data=True
        )
        
        self.team = Team.objects.create(
            name='Apple',
            is_active=True            
        )
        
        self.employee = Employee.objects.create(
            user=self.user,
            team=self.team,
            is_active=True,
            access_level=self.perm_DEV,
        )
        
        self.client = APIClient()
        self.url = reverse("list-team")
    
    def test_user_has_default_password(self):
        self.user.is_default_password=True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        
        response=self.client.get(self.url)
        
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["message"], "Password has not been changed")
        
    def test_user_not_part_of_any_team(self):
        self.employee.delete()
        self.client.force_authenticate(user=self.user)
        
        response=self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "User is not part of any team")