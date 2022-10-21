from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListAPIView(generics.ListAPIView):
  serializer_class = CategorySerializer

  def get_queryset(self):
    return Category.objects.filter(state=True)


class ProductListAPIView(generics.ListCreateAPIView):
  serializer_class = ProductSerializer
  queryset = ProductSerializer.Meta.model.objects.filter(state = True)

  def post(self, request):
    product_serializer = ProductSerializer(data = request.data)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
