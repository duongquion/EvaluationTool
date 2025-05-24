from rest_framework import serializers

from ..models import (
    InputType
)

class InputTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InputType
        fields = "__all__"