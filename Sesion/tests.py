from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Producto

class ProductoModelTest(TestCase):
    def test_crear_producto(self):
        producto = Producto.objects.create(
            idProducto=1,
            nombreProducto="Crema Facial",
            tipoProducto="Cuidado",
            marcaProducto="Nivea",
            precioDeProducto=25000,
            cantidadDeProducto=10,
            fechaVencimientoProducto="2026-01-01"
        )

        self.assertEqual(producto.nombreProducto, "Crema Facial")
        self.assertEqual(producto.precioDeProducto, 25000)
        self.assertEqual(producto.cantidadDeProducto, 10)
        self.assertTrue(isinstance(producto, Producto))


from django.test import TestCase
from .models import Usuario, Sesion, Reseña

class ReviewTest(TestCase):
    def test_crear_resena(self):
        # Crear usuario
        usuario = Usuario.objects.create(
            idUsuario=1,
            nombreCompletoUsuario="Gabriela Sanabria",
            correoUsuario="gabi@example.com",
            contraseñaUsuario="1234",
            tipoUsuario="cliente"
        )

        # Crear sesión
        sesion = Sesion.objects.create(
            idSesion=1,
            nombreSesion="Masaje de Relajación",
            categoriaSesion="Spa",
            duracionSesion="60",
            horaSesion="10:00",
            precioSesion=50000
        )

        # Crear reseña
        resena = Reseña.objects.create(
            reseñaUsuario=usuario,
            reseñaSesion=sesion,
            calificacionReseña=5,
            comentarioReseña="Excelente servicio!"
        )

        # Pruebas
        self.assertEqual(resena.calificacionReseña, 5)
        self.assertEqual(resena.reseñaUsuario.nombreCompletoUsuario, "Gabriela Sanabria")
        self.assertEqual(resena.reseñaSesion.nombreSesion, "Masaje de Relajación")
        self.assertEqual(resena.comentarioReseña, "Excelente servicio!")
