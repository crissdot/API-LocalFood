from functools import partial
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import LocalFood
from .serializers import LocalFoodSerializer

class LocalFoodAPIView(APIView):
  def get(self, request):
    local_food = LocalFood.objects.all()
    local_food_serializer = LocalFoodSerializer(local_food, many = True)
    return Response(local_food_serializer.data)

  def post(self, request):
    local_food_serializer = LocalFoodSerializer(data = request.data)
    if local_food_serializer.is_valid():
      local_food_serializer.save()
      return Response(local_food_serializer.data, status=status.HTTP_201_CREATED)
    return Response(local_food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocalFoodDetailAPIView(APIView):
  def get_localfood(self, pk):
    try:
      return LocalFood.objects.get(pk=pk)
    except LocalFood.DoesNotExist:
      raise Http404

  def get(self, request, pk):
    local_food = self.get_localfood(pk)
    local_food_serializer = LocalFoodSerializer(local_food)
    return Response(local_food_serializer.data)

  def patch(self, request, pk):
    local_food = self.get_localfood(pk)
    local_food_serializer = LocalFoodSerializer(local_food, data=request.data, partial=True)
    if local_food_serializer.is_valid():
      local_food_serializer.save()
      return Response(local_food_serializer.data)
    return Response(local_food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    local_food = self.get_localfood(pk)
    local_food.delete()
    return Response({'detail': 'Negocio eliminado correctamente'})
