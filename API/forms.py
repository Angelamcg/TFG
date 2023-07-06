from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Proveedor, Cliente

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_empresa', 'cif', 'email', 'telefono', 'web']
        widgets = {
            'telefono': forms.TextInput(attrs={'type': 'tel'}),
            'web': forms.TextInput(attrs={'type': 'url'}),
        }
        labels = {
            'nombre_empresa': 'Nombre de la empresa',
            'cif': 'CIF',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'web': 'Sitio web',
        }
        error_messages = {
            'nombre_empresa': {'required': 'Este campo es obligatorio.'},
            'cif': {'required': 'Este campo es obligatorio.', 'unique': 'Este CIF ya está en uso.'},
            'email': {'required': 'Este campo es obligatorio.'},
            'telefono': {'required': 'Este campo es obligatorio.'},
            'web': {'required': 'Este campo es obligatorio.'},
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_empresa', 'cif', 'email', 'telefono', 'web']
        widgets = {
            'telefono': forms.TextInput(attrs={'type': 'tel'}),
            'web': forms.TextInput(attrs={'type': 'url'}),
        }
        labels = {
            'nombre_empresa': 'Nombre de la empresa',
            'cif': 'CIF',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'web': 'Sitio web',
        }
        error_messages = {
            'nombre_empresa': {'required': 'Este campo es obligatorio.'},
            'cif': {'required': 'Este campo es obligatorio.', 'unique': 'Este CIF ya está en uso.'},
            'email': {'required': 'Este campo es obligatorio.'},
            'telefono': {'required': 'Este campo es obligatorio.'},
            'web': {'required': 'Este campo es obligatorio.'},
        }