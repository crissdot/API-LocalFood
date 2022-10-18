from rest_framework import generics

from ..models import Category, Product
from .serializers import CategorySerializer

class CategoryListAPIView(generics.ListAPIView):
  serializer_class = CategorySerializer

  def get_queryset(self):
    return Category.objects.filter(state=True)
