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
    reservaSesion = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name="sesion", null=True, blank=True)
 
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
    usuario = models.ForeignKey(
        'Usuario', 
        on_delete=models.CASCADE, 
        related_name='reservas', 
        null=True, 
        blank=True
    )
    fechaReserva = models.DateField(auto_now_add=True)
    horaReserva = models.TimeField(auto_now_add=True)
    precioFinalReserva = models.FloatField(default=0.0)  # 👈 inicializa en 0
    numeroPersonasReserva = models.IntegerField(null=True, blank=True)
    reservaCupon = models.OneToOneField(
        'Cupon', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    # 👇 aquí agregamos las relaciones ManyToMany
    productos = models.ManyToManyField(
        'Producto', 
        blank=True, 
        related_name='reservas'
    )
    sesiones = models.ManyToManyField(
        'Sesion', 
        blank=True, 
        related_name='reservas'
    )

    def __str__(self):
        return f"Reserva {self.idReserva} de {self.usuario.nombreCompletoUsuario}"

    

class Usuario(models.Model):
    
    idUsuario = models.AutoField(primary_key = True)
    nombreCompletoUsuario = models.CharField()
    correoUsuario = models.CharField()
    contraseñaUsuario = models.CharField()
    tipoUsuario = models.CharField(
        max_length=10,
        choices=[("cliente", "Cliente"), ("admin", "Administrador")],
        default="cliente"
    )

    def __str__(self):
        return self.nombreCompletoUsuario
    
class Cupon(models.Model):

    idCupon = models.AutoField(primary_key = True)
    descuentoCupon = models.IntegerField()
    codigoCupon = models.CharField()
    estadoCupon = models.BooleanField()
    fechaVencimientoCupon = models.DateField()

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=100)
    tipoProducto = models.CharField(max_length=50)
    marcaProducto = models.CharField(max_length=50)
    cantidadDeProducto = models.IntegerField()
    fechaVencimientoProducto = models.DateField(null=True, blank=True)
    precioDeProducto = models.FloatField()
    imagenProducto = models.ImageField(upload_to="productos/", null=True, blank=True)

    def __str__(self):
        return self.nombreProducto


