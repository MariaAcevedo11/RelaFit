# api/urls.py
from rest_framework import routers
from .views import ProductoViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductoViewSet)

urlpatterns = router.urls

