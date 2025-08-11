from django.db import models
 
# Create your models here.


class Sesion(models.Model):

    idSesion = models.IntegerField(primary_key= True)
    nombreSesion = models.CharField()
    categoriaSesion = models.CharField()
    descripcionSesion = models.TextField()
    precioSesion = models.FloatField()
    imagenSesion = models.CharField()
    duracionSesion = models.IntegerField() #en minutos
    horaSesion = models.CharField()
    disponibleSesion = models.BooleanField()

    def __str__(self):
        return self.nombreSesion

class Reseña(models.Model):

    idReseña =  models.IntegerField(primary_key= True)
    comentarioReseña = models.TextField()
    calificacionResñea = models.FloatField()
    fechaReseña = models.DateField()
    reseñaSesion = models.ForeignKey('Sesion', on_delete=models.CASCADE, related_name='reseña')

    def __str__(self):
        return f"Reseña de {self.usuario.username} - {self.reseñaSesion.nombreSesion}"
    

class Reserva(models.Model):

    idReserva = models.IntegerField(primary_key= True)
    fechaReserva = models.DateField()
    horaReserva = models.CharField()
    precioFinalReserva = models.FloatField()

    def __str__(self):
        return f"Reserva {self.idReserva} de {self.usuario.username}"

class Usuario(models.Model):
    
    idUsuario = models.IntegerField(primary_key = True)
    nombreCompletoUsuario = models.CharField()
    correoUsuario = models.CharField()
    contraseñaUsuario = models.CharField()

    def __str__(self):
        return self.nombreCompletoUsuario