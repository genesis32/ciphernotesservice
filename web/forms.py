from django import forms

class SetupForm(forms.Form):
    name = forms.CharField(max_length=20)
    public_key  = forms.FileField()
    private_key = forms.FileField()
