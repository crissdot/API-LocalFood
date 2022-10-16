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

  elif request.method == 'POST':
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def user_detail_api_view(request, pk=None):

  if request.method == 'GET':
    try:
      user = User.objects.get(pk=pk)
      user_serializer = UserSerializer(user)
      return Response(user_serializer.data)
    except User.DoesNotExist:
      raise Http404

  elif request.method == 'PATCH':
    try:
      user = User.objects.get(pk=pk)
      user_serializer = UserSerializer(user, data=request.data, partial=True)
      if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
      return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
      raise Http404

  elif request.method == 'DELETE':
    try:
      user = User.objects.get(pk=pk)
      user.delete()
      return Response({'detail': 'Usuario eliminado correctamente'})
    except User.DoesNotExist:
      raise Http404
