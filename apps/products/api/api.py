from django.http import Http404
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
  queryset = Product.objects.filter(state = True)

  def post(self, request):
    product_serializer = ProductSerializer(data = request.data)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProductSerializer

  def get_queryset(self, pk=None):
    if pk is None:
      return Product.objects.filter(state = True)
    try:
      return Product.objects.filter(id=pk, state = True)
    except Product.DoesNotExist:
      raise Http404

  def patch(self, request, pk=None):
    product = self.get_queryset(pk)
    product_serializer = ProductSerializer(product, data=request.data, partial=True)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None):
    product = self.get_queryset(pk)
    product.state = False
    product.save()
    return Response({'detail': 'Producto eliminado correctamente'})
