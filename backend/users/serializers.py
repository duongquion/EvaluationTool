from rest_framework import serializers
from users.models import (
    CustomUser as User,

)
from .utils import check_format_password

class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    new_password = serializers.CharField(validators=[check_format_password])