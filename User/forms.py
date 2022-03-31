from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=4096,required=True)