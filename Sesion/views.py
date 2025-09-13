from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Usuario, Reseña, Sesion, Producto, Reserva
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm, SesionForm
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse_lazy




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

        # Calcular promedio de las reseñas
        promedio = sesion.reseñas.aggregate(promedio=Avg('calificacionReseña'))['promedio']

        return render(request, "sesion.html", {
            "sesion": sesion,
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
            request.session['usuario_tipo'] = usuario.tipoUsuario

            print("Usuario:", usuario.nombreCompletoUsuario, "tipo:", usuario.tipoUsuario)

            if usuario.tipoUsuario == "admin":
                return redirect("productos_list")
            else:
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
        nombre = self.request.GET.get("nombre")  # 👈 nuevo filtro

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
    template_name = "reserva.html"

    def post(self, request, *args, **kwargs):
        
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return redirect("login")
        usuario = get_object_or_404(Usuario, idUsuario=request.session["usuario_id"])
        reserva = Reserva.objects.filter(usuario=usuario, estado='activa').first()

        # Confirmar reserva
        if 'confirmar' in request.POST:
            reserva.estado = 'enviada'
            reserva.save()
            messages.success(request, "¡Reserva confirmada! Muchas gracias por tu preferencia.")
            return redirect('home')

        # Eliminar producto
        eliminar_producto_id = request.POST.get("eliminar_producto_id")
        if eliminar_producto_id:
            producto = get_object_or_404(Producto, idProducto=eliminar_producto_id)
            reserva.productos.remove(producto)
            messages.error(request, f"{producto.nombreProducto} fue eliminado de tu reserva.")  # 🔴 mensaje rojo

        # Eliminar sesión
        eliminar_sesion_id = request.POST.get("eliminar_sesion_id")
        if eliminar_sesion_id:
            sesion = get_object_or_404(Sesion, idSesion=eliminar_sesion_id)
            reserva.sesiones.remove(sesion)
            messages.error(request, f"{sesion.nombreSesion} fue eliminada de tu reserva.")  # 🔴 mensaje rojo

        # Agregar producto o sesión como antes...
        producto_id = request.POST.get("producto_id")
        if producto_id:
            producto = get_object_or_404(Producto, idProducto=producto_id)
            reserva.productos.add(producto)
            messages.success(request, f"{producto.nombreProducto} agregado a tu reserva.")

        sesion_id = request.POST.get("sesion_id")
        if sesion_id:
            sesion = get_object_or_404(Sesion, idSesion=sesion_id)
            reserva.sesiones.add(sesion)
            messages.success(request, f"{sesion.nombreSesion} agregada a tu reserva.")

        # Recalcular total dinámicamente
        total = sum([p.precioDeProducto for p in reserva.productos.all()]) + \
                sum([s.precioSesion for s in reserva.sesiones.all()])
        reserva.precioFinalReserva = total
        reserva.save()

        return redirect("reserva")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_id = self.request.session.get("usuario_id")
        if usuario_id:
            usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
            reserva = Reserva.objects.filter(usuario=usuario).first()
            if reserva:
                # Recalcular precioFinalReserva dinámicamente
                total = sum([p.precioDeProducto for p in reserva.productos.all()]) + \
                        sum([s.precioSesion for s in reserva.sesiones.all()])
                reserva.precioFinalReserva = total
                reserva.save()
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
    template_name = "productos_list.html"
    context_object_name = "productos"

class ProductoCreateView(AdminRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto_form.html"
    success_url = reverse_lazy("productos_list")


class ProductoUpdateView(AdminRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto_form.html"
    success_url = reverse_lazy("productos_list")


class ProductoDeleteView(AdminRequiredMixin, DeleteView):
    model = Producto
    template_name = "producto_confirm_delete.html"
    success_url = reverse_lazy("productos_list")


# CRUD de sesiones

class SesionListView(AdminRequiredMixin, ListView):
    model = Sesion
    template_name = "sesiones_list.html"
    context_object_name = "sesiones"


class SesionCreateView(AdminRequiredMixin, CreateView):
    model = Sesion
    form_class = SesionForm
    template_name = "sesion_form.html"
    success_url = reverse_lazy("sesiones_list")

class SesionUpdateView(AdminRequiredMixin, UpdateView):
    model = Sesion
    form_class = SesionForm
    template_name = "sesion_form.html"
    success_url = reverse_lazy("sesiones_list")


class SesionDeleteView(AdminRequiredMixin, DeleteView):
    model = Sesion
    template_name = "sesion_confirm_delete.html"
    success_url = reverse_lazy("sesiones_list")




    
