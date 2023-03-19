from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

from ..models import User
from .serializers import UserSerializer, PasswordSerializer
from apps.base.authentication import Authentication
from apps.base.permissions import IsAuthenticatedAndOwnerUserOrCreateOne
from apps.localfood.api.serializers import LocalFoodSerializer
from apps.products.models import Product
from apps.products.api.serializers import ProductSerializer

class UserViewSet(viewsets.GenericViewSet):
  serializer_class = UserSerializer
  queryset = None
  authentication_classes = (Authentication, )
  permission_classes = (IsAuthenticatedAndOwnerUserOrCreateOne, )

  def get_object(self, request, pk):
    user = get_object_or_404(User, pk=pk, is_active=True)
    self.check_object_permissions(request, user)
    return user

  # We would need this method in the future

  # def get_queryset(self):
  #   if self.queryset is None:
  #     self.queryset = User.objects.filter(is_active = True)
  #   return self.queryset

  # def list(self, request):
  #   """
  #   Obtener todos los usuarios

  #   Retorna un array con todos los usuarios existentes, en caso de no haber niguno retorna un array vacío
  #   """
  #   user = self.get_queryset()
  #   user_serializer = UserSerializer(user, many=True)
  #   return Response(user_serializer.data)

  def retrieve(self, request, pk=None):
    """
    Obtener un usuario

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna un único objeto con la información del usuario, en caso de no existir retorna un error 404
    """
    user = self.get_object(request, pk)
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

    RUTA PROTEGIDA, SOLO DUEÑO

    Se deben envíar los campos contraseña y confirmar contraseña en atributos password y password2 respectivamente,
    se verifica que ambos sean exactamente iguales y de ser así devuelve la contraseña se actualizó correctamente
    """
    user = self.get_object(request, pk)
    password_serializer = PasswordSerializer(data=request.data)
    if password_serializer.is_valid():
      user.set_password(password_serializer.validated_data['password'])
      user.save()
      return Response({'mensaje': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
    return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    """
    Actualiza un usuario

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    NOTA Es necesario enviar todos los campos para actualizar correctamente
    """
    user = self.get_object(request, pk)
    user_serializer = UserSerializer(user, data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def partial_update(self, request, pk=None):
    """
    Actualiza parcialmente un usuario

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna el objeto ya actualizado, o en caso de no existir un error 404
    """
    user = self.get_object(request, pk)
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk=None):
    """
    Elimina lógicamente un usuario

    RUTA PROTEGIDA, SOLO DUEÑO

    Retorna un mensaje indicando que se ha eliminado correctamente, o en caso de no existir un error 404
    """
    user = self.get_object(request, pk)
    user.is_active = False
    user.save()
    return Response({'detail': 'Usuario eliminado correctamente'})

  @action(detail=True, url_path='favorite-localfoods')
  def favorite_localfoods(self, request, pk=None):
    """
    Obtener los negocios favoritos para un usuario

    RUTA PROTEGIDA, SOLO DUEÑO

    Dado el token obtenido se buscará sus negocios favoritos
    """
    if request.user is None or request.user.id != int(pk):
      return Response({'detail': 'Es necesario enviar un token de autenticación válido para este usuario'}, status=status.HTTP_401_UNAUTHORIZED)
    user = self.get_object(request, pk)

    localfood_serializer = LocalFoodSerializer(user.favs, many=True)
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

    # This is true if the current user has added to fav
    if request.user is not None:
      for localfood in localfoods:
        localfood['added_to_fav'] = True

    return Response(localfoods)
