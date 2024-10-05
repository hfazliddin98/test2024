from django import forms
from malumot.models import Mavzular



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class MavzularForm(forms.ModelForm):
    class Meta:
        model = Mavzular
        fields = [
            'mavzu'
        ]