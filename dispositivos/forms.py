from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo Electrónico", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    from django import forms


class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, label="Correo Electrónico")
    company_name = forms.CharField(max_length=255, required=True, label="Nombre de la Empresa")

    class Meta:
        model = User
        fields = ['company_name', 'email', 'password1', 'password2']

    # Validación para asegurarse de que el correo no esté registrado
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", max_length=254)