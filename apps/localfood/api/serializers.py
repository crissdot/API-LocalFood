from rest_framework import serializers
from ..models import LocalFood

class LocalFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = LocalFood
    exclude = ('is_active', 'deleted_at', 'modified_at', 'created_at')
