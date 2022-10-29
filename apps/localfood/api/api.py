from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from ..models import LocalFood
from .serializers import LocalFoodSerializer
from apps.user.authentication_mixins import AuthenticationOrReadOnly

class LocalFoodViewSet(viewsets.GenericViewSet):
  serializer_class = LocalFoodSerializer
  queryset = None
  authentication_classes = (AuthenticationOrReadOnly, )

  def get_object(self, pk):
    return get_object_or_404(LocalFood, pk=pk)

  def get_queryset(self):
    if self.queryset is None:
      self.queryset = LocalFood.objects.filter(is_active = True)
    return self.queryset

  def list(self, request):
    """
    Obtener todos los negocios

    Retorna un array con todos los negocios existentes, en caso de no haber niguno retorna un array vacío
    """
    localfood = self.get_queryset()
    localfood_serializer = LocalFoodSerializer(localfood, many=True)
    return Response(localfood_serializer.data)

  def retrieve(self, request, pk=None):
    """
    Obtener un negocio

    Retorna un único objeto con la información del negocio, en caso de no existir retorna un error 404
    """
    localfood = self.get_object(pk)
    localfood_serializer = LocalFoodSerializer(localfood)
    return Response(localfood_serializer.data)

  def create(self, request):
    """
    Crear un negocio

    Retorna el objeto creado con su id, o un error 400 si no cumple con las validaciones
    """
    localfood_serializer = LocalFoodSerializer(data = request.data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data, status=status.HTTP_201_CREATED)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    """
    Actualiza un negocio

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    NOTA Es necesario enviar todos los campos para actualizar correctamente
    """
    localfood = self.get_object(pk)
    localfood_serializer = LocalFoodSerializer(localfood, data=request.data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    """
    Actualiza parcialmente un negocio

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    """
    localfood = self.get_object(pk)
    localfood_serializer = LocalFoodSerializer(localfood, data=request.data, partial=True)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    """
    Elimina lógicamente un negocio

    Retorna un mensaje indicando que se ha eliminado correctamente, o en caso de no existir un error 404
    """
    localfood = self.get_object(pk)
    localfood.is_active = False
    localfood.save()
    return Response({'detail': 'Negocio eliminado correctamente'})
