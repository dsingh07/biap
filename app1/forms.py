from django.contrib.auth.models import User
from django import forms

# Forms for user for registration with password set so that it is invisible during input
# Other parameters for registration: username, email
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')