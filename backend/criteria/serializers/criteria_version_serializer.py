from rest_framework import serializers
from ..models import(
    CriteriaVersion,
    CriteriaRoleEnum,
    CriteriaVersionStateEnum
)
from ..constants import(
    CriteriaVersionMessage
)
class CriteriaVersionSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(
        choices=CriteriaVersionStateEnum.choices,
        required=False
    )
    role_name = serializers.ChoiceField(
        choices=CriteriaRoleEnum.choices,
        required=False
    )
    created_user=serializers.UUIDField(read_only=True)
    updated_user=serializers.UUIDField(read_only=True)
    
    class Meta:
        model = CriteriaVersion
        fields = "__all__"
        
    def validate(self, data):
        request=self.context.get("context", None)
        if request and request.method in ["PUT", "PATCH"]:
            attr_list = list(data.values())
            if len(attr_list) != 1:
                raise serializers.ValidationError(
                    CriteriaVersionMessage.ONLY_ONE_FIELD_CAN_BE_UPDATED
                )
            
        return data