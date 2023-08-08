from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
