from django import forms

from core.models import User

class AuthRequestForm(forms.Form):
    mobile_user = forms.ModelChoiceField(queryset=User.objects.none())
    authorization_code = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('mobile_user')
        super(AuthRequestForm, self).__init__(*args, **kwargs)
        self.fields['mobile_user'].queryset = qs

