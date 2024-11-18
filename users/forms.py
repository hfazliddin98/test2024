from django import forms
from users.models import Fakultets, Yonalishs, Kurs, Guruhs


class YonalishsForm(forms.ModelForm):
    ism = forms.CharField(max_length=255)
    kurs = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': "Yo`nalishni kiriting"}),
        queryset=Kurs.objects.all()
    )


    class Meta:
        model = Yonalishs
        fields = ['fakultet', 'name', 'ism', 'kurs']

