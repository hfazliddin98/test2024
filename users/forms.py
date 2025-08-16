
from django import forms
from users.models import Users, Yonalishs, Kurs, Fakultets, Guruhs


# O‘qituvchi (teacher) form

class OqituvchiForm(forms.ModelForm):
    password = forms.CharField(label='Parol', widget=forms.PasswordInput(render_value=True), required=True)
    password2 = forms.CharField(label='Parolni tasdiqlash', widget=forms.PasswordInput(render_value=True), required=True)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['first_name'].widget.attrs['autocomplete'] = 'off'
        self.fields['last_name'].widget.attrs['autocomplete'] = 'off'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Parollar mos emas!')
        return cleaned_data


# Fakultet form
class FakultetForm(forms.ModelForm):
    class Meta:
        model = Fakultets
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fakultet nomi'})
        }

# Yonalish form
class YonalishForm(forms.ModelForm):
    class Meta:
        model = Yonalishs
        fields = ['name', 'fakultet']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yo‘nalish nomi'}),
            'fakultet': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Yo‘nalish nomi',
            'fakultet': 'Fakultet',
        }
        error_messages = {
            'name': {
                'required': 'Yo‘nalish nomi kiritilishi shart.',
            },
            'fakultet': {
                'required': 'Fakultet tanlanishi shart.',
            },
        }

# Kurs form
class KursForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = ['name', 'yonalish']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kurs nomi'}),
            'yonalish': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Kurs nomi',
            'yonalish': 'Yo‘nalish',
        }
        error_messages = {
            'name': {
                'required': 'Kurs nomi kiritilishi shart.',
            },
            'yonalish': {
                'required': 'Yo‘nalish tanlanishi shart.',
            },
        }

# Guruh form
class GuruhForm(forms.ModelForm):
    class Meta:
        model = Guruhs
        fields = ['name', 'kurs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guruh nomi'}),
            'kurs': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Guruh nomi',
            'kurs': 'Kurs',
        }
        error_messages = {
            'name': {
                'required': 'Guruh nomi kiritilishi shart.',
            },
            'kurs': {
                'required': 'Kurs tanlanishi shart.',
            },
        }

