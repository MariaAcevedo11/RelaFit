from django.urls import path 
from .views import HomePageView, LoginPageView, RegistroPageView, ProductoPageView, LogoutPageView, CarritoPageView, SesionPageView 
'''AgregarReseñaView,'''
''' path("sesion/<int:sesion_id>/reseña/", AgregarReseñaView.as_view(), name="agregarReseña"),'''
urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'), 
    path("login/", LoginPageView.as_view(), name = 'login'),
    path("registro/", RegistroPageView.as_view(), name = 'registro'),
    path("producto/", ProductoPageView.as_view() , name = 'producto'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path("carrito/", CarritoPageView.as_view(), name = 'carrito'),
    path("sesion/<int:sesion_id>/", SesionPageView.as_view(), name="detalleSesion"),
   

]