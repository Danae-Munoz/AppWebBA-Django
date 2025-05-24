from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['idprod', 'nomprod', 'descprod', 'precio', 'imagen']

class IniciarSesionForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Cuenta")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=20, required=True, label="RUT")
    dirusu = forms.CharField(max_length=300, required=True, label="Dirección")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rut', 'dirusu']

    def save(self, commit=True):
        user = super().save(commit=False)  # solo guarda el User, no aún en la DB
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                dirusu=self.cleaned_data['dirusu'],
                tipousu='Cliente'  # o según tu lógica
            )
        return user
class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=20, required=False, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario")
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección")

    class Meta:
        fields = '__all__'