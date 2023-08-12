from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser, Subscription


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)
