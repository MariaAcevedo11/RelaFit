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
    sesionesReserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='reservas', null=True, blank=True) # relacion uno a muchos con reserva 

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

    idReserva = models.AutoField(primary_key= True)
    fechaReserva = models.DateField()
    horaReserva = models.CharField()
    precioFinalReserva = models.FloatField()
    reservasUser = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reservas', null=True, blank=True) #relacion uno a muchos con usuario
    reservaCupon = models.OneToOneField('Cupon', on_delete=models.CASCADE, null=True, blank=True) # relacion uno a uno con cupon
    numeroPersonasReserva = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return f"Reserva {self.idReserva} de {self.usuario.username}"

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
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.usuario.nombreCompletoUsuario}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precioDeProducto * self.cantidad