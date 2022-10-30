from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from ..models import User
from .serializers import UserSerializer, PasswordSerializer
from apps.base.authentication import Authentication

class UserViewSet(viewsets.GenericViewSet):
  serializer_class = UserSerializer
  queryset = None
  authentication_classes = (Authentication, )

  def get_object(self, pk):
    return get_object_or_404(User, pk=pk)

  def get_queryset(self):
    if self.queryset is None:
      self.queryset = User.objects.filter(is_active = True)
    return self.queryset

  def list(self, request):
    """
    Obtener todos los usuarios

    Retorna un array con todos los usuarios existentes, en caso de no haber niguno retorna un array vacío
    """
    user = self.get_queryset()
    user_serializer = UserSerializer(user, many=True)
    return Response(user_serializer.data)

  def retrieve(self, request, pk=None):
    """
    Obtener un usuario

    Retorna un único objeto con la información del usuario, en caso de no existir retorna un error 404
    """
    user = self.get_object(pk)
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)

  def create(self, request):
    """
    Crear un usuario

    Retorna el objeto creado con su id, o un error 400 si no cumple con las validaciones
    """
    user_serializer = UserSerializer(data = request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @swagger_auto_schema(request_body=PasswordSerializer)
  @action(detail=True, methods=['patch'], url_path='password')
  def change_password(self, request, pk=None):
    """
    Cambiar contraseña

    Se deben envíar los campos contraseña y confirmar contraseña en atributos password y password2 respectivamente,
    se verifica que ambos sean exactamente iguales y de ser así devuelve la contraseña se actualizó correctamente
    """
    user = self.get_object(pk)
    password_serializer = PasswordSerializer(data=request.data)
    if password_serializer.is_valid():
      user.set_password(password_serializer.validated_data['password'])
      user.save()
      return Response({'mensaje': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
    return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    """
    Actualiza un usuario

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    NOTA Es necesario enviar todos los campos para actualizar correctamente
    """
    user = self.get_object(pk)
    user_serializer = UserSerializer(user, data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    """
    Actualiza parcialmente un usuario

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    """
    user = self.get_object(pk)
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    """
    Elimina lógicamente un usuario

    Retorna un mensaje indicando que se ha eliminado correctamente, o en caso de no existir un error 404
    """
    user = self.get_object(pk)
    user.is_active = False
    user.save()
    return Response({'detail': 'Usuario eliminado correctamente'})
