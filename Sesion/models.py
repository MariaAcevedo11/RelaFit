#Autores: María Acevedo, Gabriela Sanabria, Jose Cardenas

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
 
# Create your models here.


class Sesion(models.Model):

    idSesion = models.AutoField(primary_key= True)
    nombreSesion = models.CharField(blank = False, null = False)
    categoriaSesion = models.CharField(blank = False, null = False)
    descripcionSesion = models.TextField(blank = False, null = False)
    imagenSesion = models.ImageField(upload_to="sesiones/" , blank = False, null = False)
    precioSesion = models.FloatField(blank = False, null = False)
    duracionSesion = models.IntegerField(blank = False, null = False) #en minutos
    horaSesion = models.CharField(blank = False, null = False)
    reservaSesion = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name="sesion", blank = True, null = True)
 
    def __str__(self):
        return self.nombreSesion

class Reseña(models.Model):

    idReseña =  models.AutoField(primary_key= True)
    comentarioReseña = models.TextField()
    calificacionReseña = models.IntegerField()
    fechaReseña = models.DateField(auto_now_add=True)
    reseñaSesion = models.ForeignKey('Sesion', on_delete=models.CASCADE, related_name='reseñas')
    reseñaUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reseñas') # relacion uno a muchos con usuario

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
    numeroPersonasReserva = models.IntegerField(blank = True, null = True)
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
    estado = models.CharField(
    max_length=20,
    choices=[('activa', 'Activa'), ('enviada', 'Enviada')],
    default='activa'
)

    def __str__(self):
        return f"Reserva {self.idReserva} de {self.usuario.nombreCompletoUsuario}"

    

class Usuario(models.Model):
    
    idUsuario = models.AutoField(primary_key = True)
    nombreCompletoUsuario = models.CharField(blank = False, null = False)
    correoUsuario = models.CharField(blank = False, null = False)
    contraseñaUsuario = models.CharField(blank = False, null = False)
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

    @property
    def activo(self):
        return self.estadoCupon and self.fechaVencimientoCupon >= timezone.now().date()

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=100, blank = False, null = False)
    tipoProducto = models.CharField(max_length=50, blank = False, null = False)
    marcaProducto = models.CharField(max_length=50, blank = False, null = False)
    cantidadDeProducto = models.IntegerField(blank = False, null = False)
    fechaVencimientoProducto = models.DateField(blank = False, null = False)
    precioDeProducto = models.FloatField(blank = False, null = False)
    imagenProducto = models.ImageField(upload_to="productos/", blank = False, null = False)

    def __str__(self):
        return self.nombreProducto