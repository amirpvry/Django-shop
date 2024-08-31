from django.contrib.auth import forms as auth_forms
from django import forms


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        super(CustomAuthenticationForm, self).confirm_login_allowed(user)