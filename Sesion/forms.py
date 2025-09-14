#Autores: María Acevedo, Gabriela Sanabria, Jose Cardenas

from .models import Reseña, Producto, Sesion, Cupon
from django import forms


class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["calificacionReseña", "comentarioReseña"]
        widgets = {
            "calificacionReseña": forms.NumberInput(
                attrs={"min": 1, "max": 5, "class": "w-20 border rounded-md px-2"}
            ),
            "comentarioReseña": forms.Textarea(
                attrs={"rows": 3, "class": "w-full border rounded-md p-2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        calificacion = cleaned_data.get("calificacionReseña")
        comentario = cleaned_data.get("comentarioReseña")

        if not calificacion:
            raise forms.ValidationError("Debes dar una calificación con estrellas.")
        if not comentario:
            raise forms.ValidationError("Debes escribir un comentario.")

        return cleaned_data
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombreProducto", "tipoProducto", "cantidadDeProducto",
            "precioDeProducto", "imagenProducto", "marcaProducto",
            "fechaVencimientoProducto"
        ]
        widgets = {
            "nombreProducto": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "tipoProducto": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "cantidadDeProducto": forms.NumberInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "precioDeProducto": forms.NumberInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "imagenProducto": forms.ClearableFileInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-2 py-1 shadow-sm"
            }),
            "marcaProducto": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "fechaVencimientoProducto": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
        }


class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = [
            "nombreSesion", "categoriaSesion", "descripcionSesion",
            "imagenSesion", "precioSesion", "duracionSesion",
            "horaSesion"
        ]
        widgets = {
            "nombreSesion": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "categoriaSesion": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "descripcionSesion": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded p-2 shadow-sm"
            }),
            "imagenSesion": forms.ClearableFileInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-2 py-1 shadow-sm"
            }),
            "precioSesion": forms.NumberInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "duracionSesion": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "horaSesion": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            })
        }

class CuponForm(forms.ModelForm):
    class Meta:
        model = Cupon
        fields = ["codigoCupon", "descuentoCupon", "estadoCupon", "fechaVencimientoCupon"]
        widgets = {
            "codigoCupon": forms.TextInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "descuentoCupon": forms.NumberInput(attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
            "estadoCupon": forms.Select(choices=[
                (True, "Activo"),
                (False, "Inactivo"),
            ], attrs={
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm bg-white"
            }),
            "fechaVencimientoCupon": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border border-pink-500 focus:border-pink-600 "
                         "focus:ring-2 focus:ring-pink-500 rounded px-4 py-2 shadow-sm"
            }),
        }