from rest_framework.routers import DefaultRouter
from .api import ProductViewSet

router = DefaultRouter()

router.register(r'', ProductViewSet, basename='Productos')

router_urls = router.urls
