from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from ..models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.GenericViewSet):
  serializer_class = CategorySerializer

  def get_queryset(self, pk=None):
    if pk is None:
      return Category.objects.filter(is_active = True)
    try:
      return Category.objects.get(id=pk, is_active = True)
    except Category.DoesNotExist:
      raise Http404

  def list(self, request):
    """
    Obtener todas las categorías

    Retorna un array con todas las categorías existentes, en caso de no haber niguno retorna un array vacío
    """
    category = self.get_queryset()
    category_serializer = CategorySerializer(category, many=True)
    return Response(category_serializer.data)

  def retrieve(self, request, pk=None):
    """
    Obtener una categoría

    Retorna un único objeto con la información de la categoría, en caso de no existir retorna un error 404
    """
    category = self.get_queryset(pk)
    category_serializer = CategorySerializer(category)
    return Response(category_serializer.data)

class ProductViewSet(viewsets.GenericViewSet):
  serializer_class = ProductSerializer

  def get_queryset(self, pk=None):
    if pk is None:
      return Product.objects.filter(is_active = True)
    try:
      return Product.objects.get(id=pk, is_active = True)
    except Product.DoesNotExist:
      raise Http404

  def list(self, request):
    """
    Obtener todos los platillos

    Retorna un array con todos los platillos existentes, en caso de no haber niguno retorna un array vacío
    """
    product = self.get_queryset()
    product_serializer = ProductSerializer(product, many=True)
    return Response(product_serializer.data)

  def retrieve(self, request, pk=None):
    """
    Obtener un platillo

    Retorna un único objeto con la información del platillo, en caso de no existir retorna un error 404
    """
    product = self.get_queryset(pk)
    product_serializer = ProductSerializer(product)
    return Response(product_serializer.data)

  def create(self, request):
    """
    Crear un platillo

    Retorna el objeto creado con su id, o un error 400 si no cumple con las validaciones
    """
    product_serializer = ProductSerializer(data = request.data)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    """
    Actualiza un platillo

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    NOTA Es necesario enviar todos los campos para actualizar correctamente
    """
    product = self.get_queryset(pk)
    product_serializer = ProductSerializer(product, data=request.data)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    """
    Actualiza parcialmente un platillo

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    """
    product = self.get_queryset(pk)
    product_serializer = ProductSerializer(product, data=request.data, partial=True)
    if product_serializer.is_valid():
      product_serializer.save()
      return Response(product_serializer.data)
    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    """
    Elimina lógicamente un platillo

    Retorna un mensaje indicando que se ha eliminado correctamente, o en caso de no existir un error 404
    """
    product = self.get_queryset(pk)
    product.is_active = False
    product.save()
    return Response({'detail': 'Producto eliminado correctamente'})
