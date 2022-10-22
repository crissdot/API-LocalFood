from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from ..models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.GenericViewSet):
  serializer_class = UserSerializer

  def get_queryset(self, pk=None):
    if pk is None:
      return User.objects.filter(state = True)
    try:
      return User.objects.get(id=pk, state = True)
    except User.DoesNotExist:
      raise Http404

  def list(self, request):
    user = self.get_queryset()
    user_serializer = UserSerializer(user, many=True)
    return Response(user_serializer.data)

  def create(self, request):
    user_serializer = UserSerializer(data = request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, pk=None):
    user = self.get_queryset(pk)
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)

  def update(self, request, pk=None):
    user = self.get_queryset(pk)
    user_serializer = UserSerializer(user, data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    user = self.get_queryset(pk)
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    user = self.get_queryset(pk)
    user.state = False
    user.save()
    return Response({'detail': 'Usuario eliminado correctamente'})
