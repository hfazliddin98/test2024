from django import forms
from malumot.models import Mavzular, Testlar



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class MavzularForm(forms.ModelForm):
    class Meta:
        model = Mavzular
        fields = [
            'mavzu'
        ]


class TestlarForm(forms.ModelForm):
    class Meta:
        model = Testlar
        fields = [
            'mavzu_id',
            'savol',
            'a',
            'b',
            'c',
            'd',
            'togri',
        ]