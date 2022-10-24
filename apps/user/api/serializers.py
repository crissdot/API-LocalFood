from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('last_login', 'is_superuser', 'is_active', 'deleted_at', 'modified_at', 'created_at')

  def create(self, validated_data):
    user = User(**validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, instance, validated_data):
    updated_user = super().update(instance, validated_data)
    updated_user.set_password(validated_data['password'])
    updated_user.save()
    return updated_user

  def to_representation(self, instance):
    return {
      'id': instance.id,
      'username': instance.username,
      'name': instance.name,
      'last_name': instance.last_name,
      'phone_number': instance.phone_number,
      'email': instance.email,
    }
