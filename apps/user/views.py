from datetime import datetime

from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from apps.user.api.serializers import UserSerializer

def delete_all_sessions(user):
  all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
  if all_sessions.exists():
    for session in all_sessions:
      session_data = session.get_decoded()
      if user.id == int(session_data.get('_auth_user_id')):
        session.delete()

class Login(ObtainAuthToken):

  def post(self, request):
    login_serializer = self.serializer_class(data=request.data, context={'request':request})
    if not login_serializer.is_valid():
      return Response({'mensaje': 'Usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

    user = login_serializer.validated_data['user']
    if not user.is_active:
      return Response({'mensaje': 'Este usuario no puede iniciar sesión'}, status=status.HTTP_403_FORBIDDEN)

    token, is_created = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    if not is_created:
      delete_all_sessions(user)

      token.delete()
      token = Token.objects.create(user=user)

    return Response({
      'token': token.key,
      'user': user_serializer.data,
      'mensaje': 'Has iniciado sesión correctamente'
    })


class Logout(APIView):
  def post(self, request):
    request_token = request.POST.get('token')
    if request_token is None:
      return Response({'mensaje': 'Debes envíar un token'}, status=status.HTTP_400_BAD_REQUEST)

    token = Token.objects.filter(key=request_token).first()
    if not token:
      return Response({'mensaje': 'No se encontró un usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)

    user = token.user
    delete_all_sessions(user)
    token.delete()
    return Response({'mensaje': 'Has cerrado sesión correctamente'})