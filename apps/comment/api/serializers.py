from rest_framework import serializers

from ..models import Comment

class CommentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Comment
    exclude = ('is_active', 'deleted_at', 'modified_at', 'created_at')

  def to_representation(self, instance):
    return {
      'id': instance.id,
      'text': instance.text,
      'user': {
        'id': instance.user.id,
        'username': instance.user.username
      },
      'created_at': instance.created_at,
    }
