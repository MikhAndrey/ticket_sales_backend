import os
import uuid

from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.models import City, Stadium
from core.response import Response
from core.serializers import CitySerializer, UserRegistrationSerializer, StadiumSerializer, StadiumGetSerializer
from ticket_sales_backend import settings


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        response = Response(model=serializer.data, message="The list of cities was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class StadiumListView(APIView):
    def get(self, request):
        query_filter = {
            'name': request.query_params.get('name') or "",
            'address': request.query_params.get('address') or ""
        }
        stadiums = Stadium.objects.all().filter(
            name__icontains=query_filter['name'],
            address__icontains=query_filter['address'])
        serializer = StadiumGetSerializer(stadiums, many=True)
        response = Response(model=serializer.data, message="The list of stadiums was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class StadiumView(APIView):
    def get(self, request, id):
        try:
            stadium = Stadium.objects.get(id=id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)
        serializer = StadiumGetSerializer(stadium)
        response = Response(model=serializer.data, message="Stadium info was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)

    def post(self, request):
        data = request.data
        file = request.FILES.get('photo')
        if file:
            file_path = self.handle_uploaded_file(file)
            data['photo_link'] = file_path
        serializer = StadiumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Stadium was created successfully")
            return JsonResponse(response.to_dict(), status=201)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def put(self, request, id):
        try:
            stadium = Stadium.objects.get(id=id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)
        data = request.data
        file = request.FILES.get('photo')
        if file:
            file_path = self.handle_uploaded_file(file)
            data['photo_link'] = file_path
        serializer = StadiumSerializer(stadium, data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Stadium info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def delete(self, request, id):
        try:
            stadium = Stadium.objects.get(id=id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)
        photo_link = stadium.photo_link
        if photo_link:
            file_path = os.path.join(settings.MEDIA_ROOT, photo_link)
            if os.path.exists(file_path):
                os.remove(file_path)
        stadium.delete()
        response = Response(message="Stadium was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)

    def handle_uploaded_file(self, file):
        folder_name = 'stadiums'
        upload_dir = os.path.join(settings.MEDIA_ROOT, folder_name)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        ext = file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return os.path.join(folder_name, filename)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(message="The user was registered successfully")
            return JsonResponse(response.to_dict(), status=201)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)
