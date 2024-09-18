
from django import forms
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from accounts.models import Profile


class CustomSetPasswordForm(forms.Form):
    """
    A form that lets a user set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("دو قسمت رمز عبور مطابقت نداشتند."),
    }
    new_password1 = forms.CharField(
        label=_("رمز جدید"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password consfirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    
    
class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        **CustomSetPasswordForm.error_messages,
        "password_incorrect": _(
            "رمز عبور قدیمی شما اشتباه وارد شده است. لطفا دوباره وارد کنید"
        ),
        }
    old_password = forms.CharField(
        label=_("رمز فعلی"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام خود را وارد نمایید'
        self.fields['last_name'].widget.attrs['class'] = 'form-control '
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی را وارد نمایید'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control text-center'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره همراه را وارد نمایید'
        