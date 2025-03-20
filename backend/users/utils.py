import re
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

def check_format_password(value):
    error_messages = {
        "lowercase": "Password must contain at least one lowercase letter.",
        "uppercase": "Password must contain at least one uppercase letter.",
        "digit": "Password must contain at least one digit.",
        "special": "Password must contain at least one special character @$!%*?&.",
        "space": "Password must not contain spaces",
        "length": "Password must be between 8 and 12 characters."
    }
    if not re.search(r"[a-z]", value):
        raise serializers.ValidationError(error_messages["lowercase"])
    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError(error_messages["uppercase"])
    if not re.search(r"\d", value):
        raise serializers.ValidationError(error_messages["digit"])
    if not re.search(r"[@$!%*?&]", value):
        raise serializers.ValidationError(error_messages["special"])
    if re.search(r"\s", value):
        raise serializers.ValidationError(error_messages["space"])
    if len(value) <= 8 & len(value) >= 12:
        raise serializers.ValidationError(error_messages["length"])
    return value