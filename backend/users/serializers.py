from rest_framework import serializers
from users.models import (
    CustomUser as User,
    Team,
)
from .utils import check_format_password

class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    new_password = serializers.CharField(validators=[check_format_password])
    
class SetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(validators=[check_format_password])
    question = serializers.CharField(max_length=150) 
    answer = serializers.CharField(max_length=150)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    new_password = serializers.CharField(validators=[check_format_password])
    answer = serializers.CharField(max_length=150)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
    
class TeamSerializer(serializers.ModelSerializer):
    parent_team = serializers.StringRelatedField()
    created_user = UserSerializer()
 
    class Meta:
        model = Team
        fields = ['id', 'name', 'parent_team', 'is_active', 'created_user', 'created_at']