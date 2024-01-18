from django import forms
from django.contrib.auth.forms import AuthenticationForm


#LoginForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(
        attrs = {
            'placeholder':'username or phone'
        }
    ))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs = {
            'placeholder': 'password'
        }
    ))
