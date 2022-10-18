from rest_framework import generics

from ..models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListAPIView(generics.ListAPIView):
  serializer_class = CategorySerializer

  def get_queryset(self):
    return Category.objects.filter(state=True)


class ProductListAPIView(generics.ListAPIView):
  serializer_class = ProductSerializer

  def get_queryset(self):
    return Product.objects.filter(state=True)
