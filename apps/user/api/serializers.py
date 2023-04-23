from rest_framework import serializers
from ..models import User
from ... import constants

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('last_login', 'is_superuser', 'is_active', 'deleted_at', 'modified_at', 'created_at')

  def validate_password(self, value):
    if len(value) < 6:
      raise serializers.ValidationError('La contraseña debe contener más de 6 caracteres')
    return value

  def create(self, validated_data):
    user = User(**validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, instance, validated_data):
    updated_user = super().update(instance, validated_data)
    try:
      updated_user.set_password(validated_data['password'])
      updated_user.save()
    except:
      print("password doesn't exist")
    return updated_user

  def to_representation(self, instance):
    return {
      'id': instance.id,
      'username': instance.username,
      'name': instance.name,
      'last_name': instance.last_name,
      'phone_number': instance.phone_number,
      'email': instance.email,
      'profile_image': instance.profile_image.url if instance.profile_image else constants.PLACEHOLDER_USER_IMAGE,
    }


class PasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=128, min_length=6, write_only=True)
  password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

  def validate(self, data):
    if data['password'] != data['password2']:
      raise serializers.ValidationError({'error': 'Las contraseñas deben ser iguales'})
    return data
