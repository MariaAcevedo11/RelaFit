from .models import Reseña
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