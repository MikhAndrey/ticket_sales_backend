from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.models import City
from core.response import Response
from core.serializers import CitySerializer, UserRegistrationSerializer


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        response = Response(model=serializer.data, message="The list of cities was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(message="The user was registered successfully")
            return JsonResponse(response.to_dict(), status=201)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)
