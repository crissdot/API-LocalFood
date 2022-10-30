from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

class Authentication(authentication.BaseAuthentication):
  user = None
  token = None

  def authenticate(self, request):
    user = self.get_user(request)
    return (user, None)

  def get_user(self, request):
    token_header = get_authorization_header(request).split()
    if not token_header:
      return None

    try:
      token_auth = TokenAuthentication()
      token_decoded = token_header[1].decode()
      user, token = token_auth.authenticate_credentials(token_decoded)
      self.user = user
      self.token = token
      return user
    except:
      raise AuthenticationFailed('Token inválido')
