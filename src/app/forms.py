from django import forms
from django.contrib.auth import forms as auth_forms, models


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomUserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm):
        model = models.User
        fields = ('username', 'email', 'password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'id_signup_username'
        self.fields['username'].label = 'Login'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'Confirm password'