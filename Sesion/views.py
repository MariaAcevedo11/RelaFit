from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Sesion

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sesiones = Sesion.objects.all()

        # filtros
        categoria = self.request.GET.get("categoria")
        duracion = self.request.GET.get("duracion")
        hora = self.request.GET.get("hora")

        if categoria:
            sesiones = sesiones.filter(categoriaSesion=categoria)
        if duracion:
            sesiones = sesiones.filter(duracionSesion=duracion)
        if hora:
            sesiones = sesiones.filter(horaSesion=hora)

        context["sesiones"] = sesiones
        context["categorias"] = Sesion.objects.values_list("categoriaSesion", flat=True).distinct()
        context["duraciones"] = Sesion.objects.values_list("duracionSesion", flat=True).distinct()
        context["horas"] = Sesion.objects.values_list("horaSesion", flat=True).distinct()

        # para mantener seleccionados
        context["categoria_seleccionada"] = categoria
        context["duracion_seleccionada"] = duracion
        context["hora_seleccionada"] = hora

        return context

class LoginPageView(TemplateView):

    template_name = "login.html"

class RegistroPageView(TemplateView):

    template_name = "registro.html"


class ProductoPageView(TemplateView):

    template_name = "producto.html"