from rest_framework import serializers

from ..models import Category, Product

class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    exclude = ('state', 'deleted_at', 'modified_at', 'created_at')


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    exclude = ('state', 'deleted_at', 'modified_at', 'created_at')
