from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

Custom_user = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Custom_user
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]


admin.site.register(Custom_user, CustomUserAdmin)
