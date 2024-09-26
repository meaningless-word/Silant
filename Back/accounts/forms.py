from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password', 'role', 'last_name', 'first_name', 'company_name', 'is_staff', 'is_active',)
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'last_name', 'first_name', 'company_name', 'is_staff', 'is_active',)