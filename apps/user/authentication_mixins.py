from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

class Authentication(object):
  user = None
  token = None

  def get_user(self, request):
    token_header = get_authorization_header(request).split()
    if not token_header:
      raise AuthenticationFailed('Debes iniciar sesión para acceder')

    try:
      token_auth = TokenAuthentication()
      token_decoded = token_header[1].decode()
      user, token = token_auth.authenticate_credentials(token_decoded)
      self.token = token
      return user
    except:
      raise AuthenticationFailed('Token inválido')


  def dispatch(self, request):
    try:
      self.user = self.get_user(request)
      return super().dispatch(request)
    except AuthenticationFailed as e:
      response = Response({'mensaje': e.detail}, status=status.HTTP_401_UNAUTHORIZED)
      response.accepted_renderer = JSONRenderer()
      response.accepted_media_type = 'application/json'
      response.renderer_context = dict()
      return response
