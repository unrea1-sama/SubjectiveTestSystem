from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=4096, required=True)
    password = forms.CharField(
        label="Password", max_length=4096, required=True, widget=forms.PasswordInput()
    )


class NewTestForm(forms.Form):
    name = forms.CharField(label="Test Name", max_length=4096, required=True)
    file = forms.FileField(allow_empty_file=False, required=True)
