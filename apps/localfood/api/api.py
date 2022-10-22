from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from ..models import LocalFood
from .serializers import LocalFoodSerializer

class LocalFoodViewSet(viewsets.GenericViewSet):
  serializer_class = LocalFoodSerializer

  def get_queryset(self, pk=None):
    if pk is None:
      return LocalFood.objects.filter(state = True)
    try:
      return LocalFood.objects.get(id=pk, state = True)
    except LocalFood.DoesNotExist:
      raise Http404

  def list(self, request):
    localfood = self.get_queryset()
    localfood_serializer = LocalFoodSerializer(localfood, many=True)
    return Response(localfood_serializer.data)

  def retrieve(self, request, pk=None):
    localfood = self.get_queryset(pk)
    localfood_serializer = LocalFoodSerializer(localfood)
    return Response(localfood_serializer.data)

  def create(self, request):
    localfood_serializer = LocalFoodSerializer(data = request.data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data, status=status.HTTP_201_CREATED)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    localfood = self.get_queryset(pk)
    localfood_serializer = LocalFoodSerializer(localfood, data=request.data)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    localfood = self.get_queryset(pk)
    localfood_serializer = LocalFoodSerializer(localfood, data=request.data, partial=True)
    if localfood_serializer.is_valid():
      localfood_serializer.save()
      return Response(localfood_serializer.data)
    return Response(localfood_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    localfood = self.get_queryset(pk)
    localfood.state = False
    localfood.save()
    return Response({'detail': 'Negocio eliminado correctamente'})
