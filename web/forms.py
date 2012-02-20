from django import forms

from core.models import User

class AuthRequestForm(forms.Form):
    mobile_users = forms.ModelChoiceField(queryset=User.objects.none())
    request = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('mobile_users')
        super(AuthRequestForm, self).__init__(*args, **kwargs)
        self.fields['mobile_users'].queryset = qs

