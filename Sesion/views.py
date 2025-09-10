from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .models import Sesion
from .models import Usuario, Reseña
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito, ItemCarrito, Producto
from django.contrib.auth.decorators import login_required
from .forms import ReseñaForm
from django.contrib import messages
from django.db.models import Avg


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



class SesionPageView(View):
    def get(self, request, sesion_id):
        sesion = get_object_or_404(Sesion, idSesion=sesion_id)

        # Calcular promedio de las reseñas
        promedio = sesion.reseñas.aggregate(promedio=Avg('calificacionReseña'))['promedio']

        return render(request, "sesion.html", {
            "sesion": sesion,
            "promedio": promedio,  # 👈 pasamos al template
        })

    def post(self, request, sesion_id):
        if not request.session.get("usuario_id"):
            return redirect("login")

        sesion = get_object_or_404(Sesion, idSesion=sesion_id)
        usuario = get_object_or_404(Usuario, idUsuario=request.session["usuario_id"])

        calificacion = request.POST.get("calificacionReseña")
        comentario = request.POST.get("comentarioReseña")

        if not calificacion or not comentario.strip():
            messages.error(request, "Debes ingresar calificación y comentario.")
            return redirect("detalleSesion", sesion_id=sesion.idSesion)

        Reseña.objects.create(
            reseñaSesion=sesion,
            reseñaUsuario=usuario,
            calificacionReseña=calificacion,
            comentarioReseña=comentario,
        )

        messages.success(request, "¡Tu reseña fue publicada con éxito!")
        return redirect("detalleSesion", sesion_id=sesion.idSesion)
    
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

class LogoutPageView(View):
    def get(self, request):
        request.session.flush()
        return redirect("login")


class ProductoPageView(TemplateView):
    
    template_name = "producto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        productos = Producto.objects.all()

        # Filtros
        marca = self.request.GET.get("marca")
        tipo = self.request.GET.get("tipo")
        precio_min = self.request.GET.get("precio_min")
        precio_max = self.request.GET.get("precio_max")

        if marca and marca != "":  
            productos = productos.filter(marcaProducto__icontains=marca)
        
        if tipo and tipo != "":  
            productos = productos.filter(tipoProducto__icontains=tipo)

        if precio_min:  
            productos = productos.filter(precioDeProducto__gte=precio_min)
        
        if precio_max:  
            productos = productos.filter(precioDeProducto__lte=precio_max)

        context["productos"] = productos

        # Para llenar los selects dinámicamente
        context["marcas"] = Producto.objects.values_list("marcaProducto", flat=True).distinct()
        context["tipos"] = Producto.objects.values_list("tipoProducto", flat=True).distinct()

        return context



## testing


class CarritoPageView(TemplateView):

    template_name = "carrito.html" 
    
    
    @login_required
    def ver_carrito(request):
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        return render(request, "carrito.html", {"carrito": carrito})


    @login_required
    def agregar_al_carrito(request, producto_id):
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        producto = get_object_or_404(Producto, idProducto=producto_id)
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not creado:
            item.cantidad += 1
            item.save()
        return redirect("ver_carrito")


    @login_required
    def eliminar_del_carrito(request, item_id):
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        item.delete()
        return redirect("ver_carrito")