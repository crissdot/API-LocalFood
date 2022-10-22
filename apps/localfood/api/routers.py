from rest_framework.routers import DefaultRouter
from .api import LocalFoodViewSet

router = DefaultRouter()

router.register(r'', LocalFoodViewSet, basename='negocios')

router_urls = router.urls
