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
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=20, required=True, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", initial='admin')
    dirusu = forms.CharField(max_length=300, required=True, label="Dirección")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'tipousu', 'rut', 'dirusu']

class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=20, required=False, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario")
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección")

    class Meta:
        fields = '__all__'