from django.forms import ModelForm
from .models import CustomUser

class CustomUserCreationForm(ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'is_staff', 'is_superuser')