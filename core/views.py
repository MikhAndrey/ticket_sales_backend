from django.http import HttpResponse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.models import City
from core.serializers import CitySerializer


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return HttpResponse(serializer.data, status=200)
