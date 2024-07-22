from django import forms

class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")
    contraseña = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
