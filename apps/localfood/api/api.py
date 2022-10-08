from rest_framework import viewsets, permissions
from ..models import LocalFood
from .serializers import LocalFoodSerializer

class LocalFoodViewSet(viewsets.ModelViewSet):
  queryset = LocalFood.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = LocalFoodSerializer
