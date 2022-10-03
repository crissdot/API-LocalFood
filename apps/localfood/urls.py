from rest_framework import routers
from .api import LocalFoodViewSet

router = routers.DefaultRouter()

router.register('negocios', LocalFoodViewSet, 'negocios')

urlpatterns = router.urls
