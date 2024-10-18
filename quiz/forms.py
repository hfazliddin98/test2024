from django import forms
from quiz.models import Mavzus, Tests



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
    def __init__(self, *args, **kwargs):
        tests = kwargs.pop('tests')
        super(TestAnswerForm, self).__init__(*args, **kwargs)
        for test, variants in tests:
            self.fields[f'test_{test.id}'] = forms.ChoiceField(
                choices=variants,
                label=test.savol,
                widget=forms.RadioSelect
            )