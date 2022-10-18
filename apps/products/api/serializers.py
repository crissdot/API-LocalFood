from rest_framework import serializers

from ..models import Category, Product

class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    exclude = ('state',)


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    exclude = ('state',)
