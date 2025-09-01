from django.urls import path 
from .views import HomePageView, LoginPageView, RegistroPageView, ProductoPageView, LogoutView

urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'), 
    path("login/", LoginPageView.as_view(), name = 'login'),
    path("registro/", RegistroPageView.as_view(), name = 'registro'),
    path("producto/", ProductoPageView.as_view() , name = 'producto'),
    path('logout/', LogoutView.as_view(), name='logout'),
]