from rest_framework.routers import DefaultRouter
from .api import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='categorias')
router.register(r'', ProductViewSet, basename='platillos')

router_urls = router.urls
