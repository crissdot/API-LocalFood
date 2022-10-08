from rest_framework import serializers
from ..models import LocalFood

class LocalFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = LocalFood
    fields = ('id', 'name', 'description')
