from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from .serializers import UserSerializer

@api_view(['GET', 'POST'])
def user_api_view(request):

  if request.method == 'GET':
    users = User.objects.all()
    users_serializers = UserSerializer(users, many=True)
    return Response(users_serializers.data)
