from rest_framework import serializers
from ..models import LocalFood

class LocalFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = LocalFood
    exclude = ('is_active', 'deleted_at', 'modified_at', 'created_at')

  def to_representation(self, instance):
    return {
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'address': instance.address,
      'phone_number': instance.phone_number,
      'schedule': instance.schedule,
      'has_delivery': instance.has_delivery,
      'social_medias': instance.social_medias,
      'profile_image': instance.profile_image.url if instance.profile_image else None,
      'banner_image': instance.banner_image.url if instance.banner_image else None,
      'owner': instance.owner.username,
    }

