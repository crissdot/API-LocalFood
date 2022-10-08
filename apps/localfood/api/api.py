from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import LocalFood
from .serializers import LocalFoodSerializer

class LocalFoodAPIView(APIView):

  def get(self, request):
    local_food = LocalFood.objects.all()
    local_food_serializer = LocalFoodSerializer(local_food, many = True)
    return Response(local_food_serializer.data)
