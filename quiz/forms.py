from django import forms
from quiz.models import Mavzus, Tests, Natijas
from .models import Fakultets, Yonalishs, Kurs, Guruhs



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class MavzusForm(forms.ModelForm):
    class Meta:
        model = Mavzus
        fields = [
            'mavzu'
        ]


class TestsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = [
            'mavzu_id',
            'savol',
            'variant_a',
            'variant_b',
            'variant_c',
            'variant_d',
            'togri_javob',
        ]

class YechishForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = [
            'mavzu_id',
            'savol',
            'variant_a',
            'variant_b',
            'variant_c',
            'variant_d',
        ]

class TestAnswerForm(forms.Form):
    talaba_name = forms.CharField(
        label="Talaba ismi",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fakultet_id = forms.ModelChoiceField(
        queryset=Fakultets.objects.all(),
        label="Fakultet",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    yonalish_id = forms.ModelChoiceField(
        queryset=Yonalishs.objects.none(),
        label="Yonalish",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    kurs_id = forms.ModelChoiceField(
        queryset=Kurs.objects.none(),
        label="Kurs",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    guruh_id = forms.ModelChoiceField(
        queryset=Guruhs.objects.none(),
        label="Guruh",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        tests = kwargs.pop('tests', None)
        super().__init__(*args, **kwargs)

        if tests:
            # Testlarni dinamik tarzda formaga qo'shish
            for test, variants in tests:
                self.fields[f'test_{test.id}'] = forms.ChoiceField(
                    label=test.savol,
                    choices=[(variant[0], variant[1]) for variant in variants],
                    widget=forms.RadioSelect
                )
                


class NatijaForm(forms.ModelForm):
    class Meta:
        model = Natijas
        fields = ['mavzu_id', 'fakultet_id', 'yonalish_id', 'kurs_id', 'guruh_id', 'talaba', 'togri', 'notogri']