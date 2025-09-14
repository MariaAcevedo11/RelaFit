from django.urls import path 
from .views import HomePageView, LoginPageView, RegistroPageView, ProductoPageView, LogoutPageView, SesionPageView, ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView, SesionListView, SesionCreateView, SesionUpdateView, SesionDeleteView, ReservaPageView, CuponListView, CuponCreateView, CuponUpdateView, CuponDeleteView

urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'), 
    path("login/", LoginPageView.as_view(), name = 'login'),
    path("registro/", RegistroPageView.as_view(), name = 'registro'),
    path("producto/", ProductoPageView.as_view() , name = 'producto'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path("reserva/", ReservaPageView.as_view(), name = 'reserva'),
    path("sesion/<int:sesion_id>/", SesionPageView.as_view(), name="detalleSesion"),
    path("panel/productos/", ProductoListView.as_view(), name="productos_list"),
    path("panel/productos/crear/", ProductoCreateView.as_view(), name="producto_form"),
    path("panel/productos/<int:pk>/editar/", ProductoUpdateView.as_view(), name="producto_form"),
    path("panel/productos/<int:pk>/eliminar/", ProductoDeleteView.as_view(), name="producto_confirm_delete"),
    path("panel/sesiones/", SesionListView.as_view(), name="sesiones_list"),
    path("panel/sesiones/crear/", SesionCreateView.as_view(), name="admin_sesion_crear"),
    path("panel/sesiones/<int:pk>/editar/", SesionUpdateView.as_view(), name="admin_sesion_editar"),
    path("panel/sesiones/<int:pk>/eliminar/", SesionDeleteView.as_view(), name="admin_sesion_eliminar"),
    path("panel/cupones/", CuponListView.as_view(), name="cupon_list"),
    path("panel/cupones/crear/", CuponCreateView.as_view(), name="cupon_form"),
    path("panel/cupones/<int:pk>/editar/", CuponUpdateView.as_view(), name="cupon_form"),
    path("panel/cupones/<int:pk>/eliminar/", CuponDeleteView.as_view(), name="cupon_delete"),

   

]