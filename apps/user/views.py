from datetime import datetime

from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from apps.user.api.serializers import UserSerializer

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
      # Delete all opened sessions
      all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
      if all_sessions.exists():
        for session in all_sessions:
          session_data = session.get_decoded()
          if user.id == int(session_data.get('_auth_user_id')):
            session.delete()

      token.delete()
      token = Token.objects.create(user=user)

    return Response({
      'token': token.key,
      'user': user_serializer.data,
      'mensaje': 'Has iniciado sesión correctamente'
    })
