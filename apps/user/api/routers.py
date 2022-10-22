from rest_framework.routers import DefaultRouter
from .api import UserViewSet

router = DefaultRouter()

router.register(r'', UserViewSet, basename='users')

router_urls = router.urls
