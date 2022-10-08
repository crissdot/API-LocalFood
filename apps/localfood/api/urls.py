from rest_framework import routers
from . import LocalFoodViewSet

router = routers.DefaultRouter()

router.register('negocios', LocalFoodViewSet, 'negocios')

urlpatterns = router.urls
