from rest_framework.routers import DefaultRouter
from .api import ProductViewSet

router = DefaultRouter()

router.register(r'', ProductViewSet, basename='platillos')

router_urls = router.urls
