from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

class Authentication(authentication.BaseAuthentication):

  def authenticate(self, request):
    user, token = self.get_auth(request)
    return (user, token)

  def get_auth(self, request):
    token_header = get_authorization_header(request).split()
    if not token_header:
      return (None, None)

    try:
      token_auth = TokenAuthentication()
      token_decoded = token_header[1].decode()
      user, token = token_auth.authenticate_credentials(token_decoded)
      return user, token
    except:
      raise AuthenticationFailed('Token inválido')
