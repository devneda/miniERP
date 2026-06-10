from django import forms
from core.models import Producto, Cliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'precio_base', 'tipo_iva', 'stock']

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock nunca puede ser inferior a 0.")
        return stock

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'nif', 'direccion', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@svalero.com'):
            raise forms.ValidationError("El email debe tener un dominio corporativo (@svalero.com).")
        return email

    def clean_nif(self):
        nif = self.cleaned_data.get('nif')
        # Aunque el modelo ya tiene unique=True, el PDF pide validarlo en el formulario
        if Cliente.objects.filter(nif=nif).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("El CIF/NIF ya existe en el sistema.")
        return nif
