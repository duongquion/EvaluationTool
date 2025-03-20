from tabulate import tabulate
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from ..models import CustomUser as User

test_results = [] # -- Global variable to store all test results --

class ChangePasswordTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\nTest Results Summary:\n")
        print(tabulate(test_results, headers=["Test Case", "HTTP Status", "Response Message"], tablefmt="grid"))
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username= 'OnDQ',
        )
        self.user.set_password("@Abcde12345")
        self.user.is_active = True
        self.user.is_default_password = False
        self.user.save()
        self.url = reverse("change-password")
        
    def test_user_does_not_exist(self):
        response= self.client.post(self.url, {
            "username":"non_user",
            "password":"oldpassword",
            "new_password":"@Newpassword1"
        })
        test_results.append(["test_user_does_not_exist", response.status_code, response.json()])
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "Username or password is incorrect")
        
    def test_user_does_not_active(self):
        self.user.is_active = False
        self.user.save()
        response= self.client.post(self.url, {
            "username":"OnDQ",
            "password":"@Abcde12345",
            "new_password":"@Newpassword1"
        })
        test_results.append(["test_user_does_not_active", response.status_code, response.json()])
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["message"], "User not allowed to do it")
        
    def test_user_has_default_password(self):
        self.user.is_default_password = True
        self.user.save()
        response= self.client.post(self.url, {
            "username":"OnDQ",
            "password":"@Abcde12345",
            "new_password":"@Newpassword1"
        })
        test_results.append(["test_user_has_default_password", response.status_code, response.json()])
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["message"], "User not allowed to do it")
        
    def test_wrong_user_old_password(self):
        response= self.client.post(self.url, {
            "username":"OnDQ",
            "password":"@Abcde12346",
            "new_password":"@Newpassword1"
        })
        test_results.append(["test_wrong_user_old_password", response.status_code, response.json()])
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "Username or password is incorrect")
        
    def test_success_change_user_password(self):
        response= self.client.post(self.url, {
            "username":"OnDQ",
            "password":"@Abcde12345",
            "new_password":"@Abcde12345"
        })
        test_results.append(["test_success_change_user_password", response.status_code, response.json()])
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Change password successfully")