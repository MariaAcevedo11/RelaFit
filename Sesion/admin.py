from django.contrib import admin

# Register your models here.

from .models import Sesion, Usuario, Producto, Reserva, Reseña, Cupon

#Para que se vean en admin y poder meter las imagenes 
admin.site.register(Sesion)
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Reserva)
admin.site.register(Reseña)
admin.site.register(Cupon)