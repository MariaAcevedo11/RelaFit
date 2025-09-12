from django.urls import path 
from .views import HomePageView, LoginPageView, RegistroPageView, ProductoPageView, LogoutPageView, CarritoPageView, SesionPageView, ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView, SesionListView, SesionCreateView, SesionUpdateView, SesionDeleteView


urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'), 
    path("login/", LoginPageView.as_view(), name = 'login'),
    path("registro/", RegistroPageView.as_view(), name = 'registro'),
    path("producto/", ProductoPageView.as_view() , name = 'producto'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path("carrito/", CarritoPageView.as_view(), name = 'carrito'),
    path("sesion/<int:sesion_id>/", SesionPageView.as_view(), name="detalleSesion"),
    path("panel/productos/", ProductoListView.as_view(), name="productos_list"),
    path("panel/productos/crear/", ProductoCreateView.as_view(), name="producto_form"),
    path("panel/productos/<int:pk>/editar/", ProductoUpdateView.as_view(), name="producto_form"),
    path("panel/productos/<int:pk>/eliminar/", ProductoDeleteView.as_view(), name="producto_confirm_delete.html"),
    path("panel/sesiones/", SesionListView.as_view(), name="sesiones_list"),
    path("panel/sesiones/crear/", SesionCreateView.as_view(), name="admin_sesion_crear"),
    path("panel/sesiones/<int:pk>/editar/", SesionUpdateView.as_view(), name="admin_sesion_editar"),
    path("panel/sesiones/<int:pk>/eliminar/", SesionDeleteView.as_view(), name="admin_sesion_eliminar"),

   

]