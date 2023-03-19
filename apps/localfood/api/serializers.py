from rest_framework import serializers
from ..models import LocalFood

class LocalFoodSerializer(serializers.ModelSerializer):
  SOCIAL_MEDIA_OPTIONS = {
    'WA': 'Whatsapp',
    'FB': 'Facebook',
    'TW': 'Twitter',
    'IG': 'Instagram',
  }

  class Meta:
    model = LocalFood
    exclude = ('is_active', 'deleted_at', 'modified_at', 'created_at')

  def validate_social_media(self, value):
    for option in value:
      if option not in self.SOCIAL_MEDIA_OPTIONS.keys():
        raise serializers.ValidationError('Ingrese una red social válida')
    return value

  def to_representation(self, instance):
    return {
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'address': instance.address,
      'phone_number': instance.phone_number,
      'schedule': instance.schedule,
      'has_delivery': instance.has_delivery,
      'social_media': (self.SOCIAL_MEDIA_OPTIONS[option] for option in instance.social_media) if instance.social_media else None,
      'profile_image': instance.profile_image.url if instance.profile_image else None,
      'banner_image': instance.banner_image.url if instance.banner_image else None,
      'owner': instance.owner.username,
      'favs': instance.favs.count(),
      'added_to_fav': False,
      'is_deleted': False if instance.is_active else True
    }

