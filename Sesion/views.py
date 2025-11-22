#Autores: María Acevedo, Gabriela Sanabria, Jose Cardenas

from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Usuario, Reseña, Sesion, Producto, Reserva, Cupon
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm, SesionForm, CuponForm
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _

#para apis

from django.http import JsonResponse
import requests
from django.conf import settings
from .services.youtube_api_service import YouTubeAPIService
from .services.local_video_service import LocalVideoService


def get_video_service():
    if getattr(settings, "VIDEO_SERVICE", "youtube") == "local":
        return LocalVideoService()
    return YouTubeAPIService()




class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        # Redirigir admin
        if request.session.get("usuario_tipo") == "admin":
            return redirect("productos_list")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtros normales
        sesiones = Sesion.objects.all()
        categoria = self.request.GET.get("categoria")
        duracion = self.request.GET.get("duracion")
        hora = self.request.GET.get("hora")
        mostrar_mejores = self.request.GET.get("mejores")  # <- nuevo parámetro

        if categoria:
            sesiones = sesiones.filter(categoriaSesion=categoria)
        if duracion:
            sesiones = sesiones.filter(duracionSesion=duracion)
        if hora:
            sesiones = sesiones.filter(horaSesion=hora)

        # Si el usuario pidió ver las mejores calificaciones
        if mostrar_mejores:
            sesiones = sesiones.annotate(promedio_reseña=Avg('reseñas__calificacionReseña'))\
                               .order_by('-promedio_reseña')[:3]

        context["sesiones"] = sesiones
        context["categorias"] = Sesion.objects.values_list("categoriaSesion", flat=True).distinct()
        context["duraciones"] = Sesion.objects.values_list("duracionSesion", flat=True).distinct()
        context["horas"] = Sesion.objects.values_list("horaSesion", flat=True).distinct()
        context["categoria_seleccionada"] = categoria
        context["duracion_seleccionada"] = duracion
        context["hora_seleccionada"] = hora
        context["mostrar_mejores"] = mostrar_mejores

        return context



class SesionPageView(View):
    
    def get(self, request, sesion_id):
        sesion = get_object_or_404(Sesion, idSesion=sesion_id)
        reseñas = sesion.reseñas.order_by('-fechaReseña')

        # Calcular promedio de las reseñas
        promedio = sesion.reseñas.aggregate(promedio=Avg('calificacionReseña'))['promedio']

        return render(request, "sesion/sesion.html", {
            "sesion": sesion,
            "reseñas": reseñas,
            "promedio": promedio,  
        })

    def post(self, request, sesion_id):
        if not request.session.get("usuario_id"):
            return redirect("login")

        sesion = get_object_or_404(Sesion, idSesion=sesion_id)
        usuario = get_object_or_404(Usuario, idUsuario=request.session["usuario_id"])

        calificacion = request.POST.get("calificacionReseña")
        comentario = request.POST.get("comentarioReseña")

        if not calificacion or not comentario.strip():
            messages.error(request, _("Debes ingresar calificación y comentario."))
            return redirect("detalle_sesion", sesion_id=sesion.idSesion)

        Reseña.objects.create(
            reseñaSesion=sesion,
            reseñaUsuario=usuario,
            calificacionReseña=calificacion,
            comentarioReseña=comentario,
        )

        messages.success(request, _("Tu reseña fue publicada con éxito!"))
        return redirect("detalle_sesion", sesion_id=sesion.idSesion)
    
class LoginPageView(View):
    template_name = "usuario/login.html"

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
            request.session['usuario_tipo'] = usuario.tipoUsuario

            print("Usuario:", usuario.nombreCompletoUsuario, "tipo:", usuario.tipoUsuario)

            if usuario.tipoUsuario == "admin":
                return redirect("productos_list")
            else:
                return redirect("home")
        except Usuario.DoesNotExist:
            return render(request, self.template_name, {"error": _("Usuario o contraseña inválidos")})
    
class RegistroPageView(TemplateView):
    template_name = "usuario/registro.html"

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
            return render(request, self.template_name, {"error": _("Las contraseñas no coinciden")})
        if Usuario.objects.filter(correoUsuario=correo).exists():
            return render(request, self.template_name, {"error": _("El correo ya está registrado")})

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
    template_name = "producto/producto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        productos = Producto.objects.all()

        # Filtros
        marca = self.request.GET.get("marca")
        tipo = self.request.GET.get("tipo")
        precio_min = self.request.GET.get("precio_min")
        precio_max = self.request.GET.get("precio_max")
        nombre = self.request.GET.get("nombre") 
        if marca:  
            productos = productos.filter(marcaProducto__icontains=marca)
        
        if tipo:  
            productos = productos.filter(tipoProducto__icontains=tipo)

        if precio_min:  
            productos = productos.filter(precioDeProducto__gte=precio_min)
        
        if precio_max:  
            productos = productos.filter(precioDeProducto__lte=precio_max)

        if nombre:  # 👈 búsqueda por nombre
            productos = productos.filter(nombreProducto__icontains=nombre)

        context["productos"] = productos

        # Para llenar los selects dinámicamente
        context["marcas"] = Producto.objects.values_list("marcaProducto", flat=True).distinct()
        context["tipos"] = Producto.objects.values_list("tipoProducto", flat=True).distinct()
        context["nombre"] = nombre  # para mantener el valor en el input

        return context


class ReservaPageView(TemplateView):
    template_name = "reserva/reserva.html"

    def post(self, request, *args, **kwargs):
        
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return redirect("login")
        usuario = get_object_or_404(Usuario, idUsuario=request.session["usuario_id"])
        # Obtiene la reserva activa o la crea
        reserva, created = Reserva.objects.get_or_create(
            usuario=usuario,
            estado="activa",
            defaults={"precioFinalReserva": 0}
        )


        # Confirmar reserva
        if 'confirmar' in request.POST:
            reserva.estado = 'enviada'
            reserva.save()
            messages.success(request, _("Reserva confirmada! Muchas gracias por tu preferencia."))
            return redirect('home')

        # Eliminar producto
        eliminar_producto_id = request.POST.get("eliminar_producto_id")
        if eliminar_producto_id:
            producto = get_object_or_404(Producto, idProducto=eliminar_producto_id)
            reserva.productos.remove(producto)
            messages.error(request, _(f"{producto.nombreProducto} fue eliminado de tu reserva."))

        # Eliminar sesión
        eliminar_sesion_id = request.POST.get("eliminar_sesion_id")
        if eliminar_sesion_id:
            sesion = get_object_or_404(Sesion, idSesion=eliminar_sesion_id)
            reserva.sesiones.remove(sesion)
            messages.error(request, _(f"{sesion.nombreSesion} fue eliminada de tu reserva."))

        # Agregar producto o sesión como antes...
        producto_id = request.POST.get("producto_id")
        if producto_id:
            producto = get_object_or_404(Producto, idProducto=producto_id)
            reserva.productos.add(producto)
            messages.success(request, _(f"{producto.nombreProducto} agregado a tu reserva."))

        sesion_id = request.POST.get("sesion_id")
        if sesion_id:
            sesion = get_object_or_404(Sesion, idSesion=sesion_id)
            reserva.sesiones.add(sesion)
            messages.success(request, _(f"{sesion.nombreSesion} agregada a tu reserva."))

        # Aplicar cupón
        codigo_cupon = request.POST.get("codigo_cupon")
        if codigo_cupon:
            try:
                cupon = Cupon.objects.get(codigoCupon=codigo_cupon, estadoCupon=True)

                # Validar vencimiento
                if cupon.fechaVencimientoCupon < timezone.now().date():
                    messages.error(request, _("El cupón está vencido."))

                # Validar si ya fue usado en otra reserva
                elif Reserva.objects.filter(reservaCupon=cupon).exists():
                    messages.error(request, _("El cupón ya fue usado en otra reserva."))

                else:
                    reserva.reservaCupon = cupon
                    cupon.estadoCupon = False
                    cupon.save()

                    messages.success(request, _(f"Cupón {codigo_cupon} aplicado con éxito."))

            except Cupon.DoesNotExist:
                messages.error(request, _("Cupón inválido."))



        # Recalcular total con cupón
        total = sum([p.precioDeProducto for p in reserva.productos.all()]) + \
                sum([s.precioSesion for s in reserva.sesiones.all()])

        if reserva.reservaCupon:
            descuento = reserva.reservaCupon.descuentoCupon
            total = total - (total * descuento / 100)

        reserva.precioFinalReserva = max(total, 0)  # nunca negativo
        reserva.save()

        return redirect("reserva")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_id = self.request.session.get("usuario_id")
        if usuario_id:
            usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
            reserva, created = Reserva.objects.get_or_create(
            usuario=usuario,
            estado="activa",
            defaults={"precioFinalReserva": 0}
        )

            if reserva:
                context["reserva"] = reserva
        return context




class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return redirect("login")  
        usuario = Usuario.objects.get(pk=usuario_id)
        if usuario.tipoUsuario != "admin":
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    

# CRUD de productos

class ProductoListView(AdminRequiredMixin, ListView):
    model = Producto
    template_name = "producto/productos_list.html"
    context_object_name = "productos"

class ProductoCreateView(AdminRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto/producto_form.html"
    success_url = reverse_lazy("productos_list")


class ProductoUpdateView(AdminRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto/producto_form.html"
    success_url = reverse_lazy("productos_list")


class ProductoDeleteView(AdminRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy("productos_list")

    def get(self, request, *args, **kwargs):
        return redirect("productos_list")

# CRUD de sesiones

class SesionListView(AdminRequiredMixin, ListView):
    model = Sesion
    template_name = "sesion/sesiones_list.html"
    context_object_name = "sesiones"


class SesionCreateView(AdminRequiredMixin, CreateView):
    model = Sesion
    form_class = SesionForm
    template_name = "sesion/sesion_form.html"
    success_url = reverse_lazy("sesiones_list")

class SesionUpdateView(AdminRequiredMixin, UpdateView):
    model = Sesion
    form_class = SesionForm
    template_name = "sesion/sesion_form.html"
    success_url = reverse_lazy("sesiones_list")


class SesionDeleteView(AdminRequiredMixin, DeleteView):
    model = Sesion
    success_url = reverse_lazy("sesiones_list")

    def get(self, request, *args, **kwargs):
        return redirect("sesiones_list")

# CRUD CUPON

class CuponListView(ListView):
    model = Cupon
    template_name = "cupon/cupon_list.html"
    context_object_name = "cupones"


class CuponCreateView(CreateView):
    model = Cupon
    form_class = CuponForm
    template_name = "cupon/cupon_form.html"
    success_url = reverse_lazy("cupon_list")


class CuponUpdateView(UpdateView):
    model = Cupon
    form_class = CuponForm
    template_name = "cupon/cupon_form.html"
    success_url = reverse_lazy("cupon_list")


class CuponDeleteView(DeleteView):
    model = Cupon
    template_name = "cupon/cupon_list"
    success_url = reverse_lazy("cupon_list")



#Consumiremos una api de youtube :) 

#Para no subir la key lol casi la kgo
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def verVideo(request):
    video_id = "Owj9PaLnB14"

    service = get_video_service()
    video = service.get_video_data(video_id)

    print(">>> API DE YOUTUBE CONSUMIDA CORRECTAMENTE")
    print(f">>> VIDEO ID UTILIZADO: {video_id}")
    print(f">>> RESPUESTA RECIBIDA: {video}")

    return render(request, "home.html", {
        "video": video,
        "video_id": video_id,
    })


# Para consumir la api de otro equipo: 


def productosAliados(request): 
    url = "http://54.90.195.251/api/products/"

    try:
        response = requests.get(url)
        productos = response.json()   # Debe llegar una lista
    except Exception as e:
        productos = []

    return render(request, "productos_aliados.html", {"productos": productos})


