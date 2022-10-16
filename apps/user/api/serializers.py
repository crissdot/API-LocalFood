from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password')

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
