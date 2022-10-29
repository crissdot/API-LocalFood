from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

class Authentication(authentication.BaseAuthentication):
  user = None
  token = None

  def authenticate(self, request):
    if request.method in permissions.SAFE_METHODS:
      return (None, None)

    user = self.get_user(request)
    return (user, None)

  def get_user(self, request):
    token_header = get_authorization_header(request).split()
    if not token_header:
      raise AuthenticationFailed('Debes iniciar sesión para acceder')

    try:
      token_auth = TokenAuthentication()
      token_decoded = token_header[1].decode()
      user, token = token_auth.authenticate_credentials(token_decoded)
      self.user = user
      self.token = token
      return user
    except:
      raise AuthenticationFailed('Token inválido')
