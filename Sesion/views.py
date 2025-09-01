from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .models import Sesion
from .models import Usuario

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

class LoginPageView(View):
    template_name = "login.html"

    def get(self, request):
        if request.session.get('usuario_id'):
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        correo = request.POST.get("email")
        contraseña = request.POST.get("password")
        try:
            usuario = Usuario.objects.get(correoUsuario=correo, contraseñaUsuario=contraseña)

            request.session['usuario_id'] = usuario.idUsuario
            request.session['usuario_nombre'] = usuario.nombreCompletoUsuario
            return redirect("home")
        except Usuario.DoesNotExist:
            return render(request, self.template_name, {"error": "Usuario o contraseña inválidos"})





class RegistroPageView(TemplateView):
    template_name = "registro.html"

    def get(self, request):
        if request.session.get('usuario_id'):
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        nombre = request.POST.get("username")
        correo = request.POST.get("email")
        contraseña = request.POST.get("password")
        contraseña2 = request.POST.get("password2")

        if contraseña != contraseña2:
            return render(request, self.template_name, {"error": "Las contraseñas no coinciden"})
        if Usuario.objects.filter(correoUsuario=correo).exists():
            return render(request, self.template_name, {"error": "El correo ya está registrado"})

        nuevo_usuario = Usuario.objects.create(
            idUsuario=Usuario.objects.count() + 1,  
            nombreCompletoUsuario=nombre,
            correoUsuario=correo,
            contraseñaUsuario=contraseña
        )

        request.session['usuario_id'] = nuevo_usuario.idUsuario
        request.session['usuario_nombre'] = nuevo_usuario.nombreCompletoUsuario

        return redirect("home")

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("login")


class ProductoPageView(TemplateView):

    template_name = "producto.html"