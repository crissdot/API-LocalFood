from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets

from ..models import LocalFood
from .serializers import LocalFoodSerializer
from apps.base.authentication import Authentication
from apps.base.permissions import IsAuthenticatedAndOwnerUserOrReadOnly
from apps.base.utils import get_data_with_new_field
from apps.products.models import Product
from apps.products.api.serializers import ProductSerializer

class LocalFoodViewSet(viewsets.GenericViewSet):
  serializer_class = LocalFoodSerializer
  queryset = None
  authentication_classes = (Authentication, )
  permission_classes = (IsAuthenticatedAndOwnerUserOrReadOnly, )

  def get_data_with_owner(self, request):
    return get_data_with_new_field(request, 'owner', request.user.id)

  def get_object(self, request, pk):
    localfood = get_object_or_404(LocalFood, pk=pk, is_active=True)
    self.check_object_permissions(request, localfood.owner)
    return localfood

  def get_queryset(self, keywords = None):
    if keywords is None:
      self.queryset = LocalFood.objects.filter(is_active = True)
    else:
      self.queryset = LocalFood.objects.filter(is_active = True, name__icontains = keywords) | LocalFood.objects.filter(is_active = True, description__icontains = keywords)
    return self.queryset

  def list(self, request):
    """
    Obtener todos los negocios

    Retorna un array con todos los negocios existentes, en caso de no haber niguno retorna un array vacío
    """
    localfood = self.get_queryset(request.GET.get('keywords', None))
    localfood_serializer = LocalFoodSerializer(localfood, many=True)
    localfoods = localfood_serializer.data

    # This includes the categories of all products inside a localfood
    if request.GET.get('categories', False):
      for localfood in localfoods:
        products = Product.objects.filter(localfood=localfood['id'], is_active=True)
        products_serializer = ProductSerializer(products, many=True)
        all_categories = list()
        for product in products_serializer.data:
          for category in all_categories:
            if category['id'] == product['category']['id']:
              break
          all_categories.append(product['category'])
        localfood['categories'] = all_categories

    return Response(localfoods)

  def retrieve(self, request, pk=None):
    """
    Obtener un negocio

    Retorna un único objeto con la información del negocio, en caso de no existir retorna un error 404
    """
    localfood = self.get_object(request, pk)
    localfood_serializer = LocalFoodSerializer(localfood)

    products_serializer = None
    if localfood is not None:
      products = Product.objects.filter(localfood=localfood.id, is_active=True)
      products_serializer = ProductSerializer(products, many=True)

    return Response({
      **localfood_serializer.data,
      'products': products_serializer.data if products_serializer else [],
    })

  def create(self, request):
    """
    Crear un negocio

    RUTA PROTEGIDA

    Retorna el objeto creado con su id, o un error 400 si no cumple con las validaciones
    """
    data = self.get_data_with_owner(request)

    localfood_serializer = LocalFoodSerializer(data=data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data, status=status.HTTP_201_CREATED)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    """
    Actualiza un negocio

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    NOTA Es necesario enviar todos los campos para actualizar correctamente
    """
    data = self.get_data_with_owner(request)
    localfood = self.get_object(request, pk)

    localfood_serializer = LocalFoodSerializer(localfood, data=data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    """
    Actualiza parcialmente un negocio

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    """
    data = self.get_data_with_owner(request)
    localfood = self.get_object(request, pk)

    localfood_serializer = LocalFoodSerializer(localfood, data=data, partial=True)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    """
    Elimina lógicamente un negocio

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna un mensaje indicando que se ha eliminado correctamente, o en caso de no existir un error 404
    """
    localfood = self.get_object(request, pk)
    localfood.is_active = False
    localfood.save()
    return Response({'detail': 'Negocio eliminado correctamente'})

  @action(detail=True, methods=['post'])
  def restore(self, request, pk=None):
    """
    Restaurar negocio

    RUTA PROTEGIDA, SOLO DUEÑO

    Simplemente al llamar este método en caso que el usuario haya eliminado su restuarante este será restaurado, caso contrario
    no se hará nada
    """
    localfood = get_object_or_404(LocalFood, pk=pk, is_active=False)
    self.check_object_permissions(request, localfood.owner)
    localfood.is_active = True
    localfood.save()
    return Response({'detail': 'Negocio restaurado correctamente'})
