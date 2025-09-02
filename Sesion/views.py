
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Sesion
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito, ItemCarrito, Producto
from django.contrib.auth.decorators import login_required

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

""" class CarritoPageView(TemplateView):
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
"""