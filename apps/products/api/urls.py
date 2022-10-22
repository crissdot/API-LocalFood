from django.urls import path
from .api import CategoryListAPIView
from .routers import router_urls

urls = [
  path('categorias/', CategoryListAPIView.as_view(), name='categorias'),
]

urlpatterns = urls + router_urls
