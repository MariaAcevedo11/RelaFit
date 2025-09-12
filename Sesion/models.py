from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.


class Sesion(models.Model):

    idSesion = models.AutoField(primary_key= True)
    nombreSesion = models.CharField()
    categoriaSesion = models.CharField()
    descripcionSesion = models.TextField()
    imagenSesion = models.ImageField(upload_to="sesiones/", blank=True, null=True)
    precioSesion = models.FloatField()
    duracionSesion = models.IntegerField() #en minutos
    horaSesion = models.CharField()
    disponibleSesion = models.BooleanField()
    reservaSesion = models.OneToOneField('Reserva', on_delete=models.CASCADE, related_name="sesion", null=True, blank=True)
 
    def __str__(self):
        return self.nombreSesion

class Reseña(models.Model):

    idReseña =  models.AutoField(primary_key= True)
    comentarioReseña = models.TextField()
    calificacionReseña = models.IntegerField()
    fechaReseña = models.DateField(auto_now_add=True)
    reseñaSesion = models.ForeignKey('Sesion', on_delete=models.CASCADE, related_name='reseñas', null=True, blank=True)
    reseñaUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reseñas', null=True, blank=True) # relacion uno a muchos con usuario

    def __str__(self):
        return f"Reseña de {self.reseñaUsuario.nombreCompletoUsuario} - {self.reseñaSesion.nombreSesion}"
    

class Reserva(models.Model):
    idReserva = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reservas', null = True, blank = True)
    fechaReserva = models.DateField(auto_now_add=True)
    horaReserva = models.TimeField(auto_now_add=True)
    precioFinalReserva = models.FloatField()
    numeroPersonasReserva = models.IntegerField(null=True, blank=True)
    reservaCupon = models.OneToOneField('Cupon', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.idReserva} de {self.usuario.nombreCompletoUsuario}"
    

class ItemReserva(models.Model):
    reservaItem = models.ForeignKey(Reserva, related_name="items", on_delete=models.CASCADE)
    productoItem = models.ForeignKey('Producto', on_delete=models.CASCADE, null=True, blank=True)
    sesionItem = models.ForeignKey(Sesion, on_delete=models.CASCADE, null=True, blank=True)
    cantidadItem = models.PositiveIntegerField(default=1)
    precioUnitarioItem = models.FloatField()

    def subtotal(self):
        return self.precioUnitario * self.cantidad



class Usuario(models.Model):
    
    idUsuario = models.AutoField(primary_key = True)
    nombreCompletoUsuario = models.CharField()
    correoUsuario = models.CharField()
    contraseñaUsuario = models.CharField()

    def __str__(self):
        return self.nombreCompletoUsuario
    
class Cupon(models.Model):

    idCupon = models.AutoField(primary_key = True)
    descuentoCupon = models.IntegerField()
    codigoCupon = models.CharField()
    estadoCupon = models.BooleanField()
    fechaVencimientoCupon = models.DateField()

class Producto(models.Model):

    idProducto = models.AutoField(primary_key = True)
    nombreProducto = models.CharField(blank=True, null=True)
    tipoProducto = models.CharField()
    cantidadDeProducto = models.IntegerField()
    precioDeProducto = models.IntegerField()
    imagenProducto = models.ImageField(upload_to="productos/", blank=True, null=True)
    marcaProducto = models.CharField()
    fechaVencimientoProducto = models.DateField()
    productoReserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='productos', null=True, blank=True)

class Carrito(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="carrito", null = True, blank = True)

    def __str__(self):
        return f"Carrito de {self.usuario.nombreCompletoUsuario}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        if self.producto:
            return self.producto.precioDeProducto * self.cantidad
        if self.sesion:
            return self.sesion.precioSesion * self.cantidad
        return 0

