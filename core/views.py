import os
import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.models import City, Stadium, Hall, Place, Event
from core.response import Response, PageResponse
from core.serializers import CitySerializer, UserRegistrationSerializer, StadiumSerializer, StadiumGetSerializer, \
    HallSerializer, HallGetSerializer, PlaceGetSerializer, PlaceSerializer, EventAnnouncementSerializer
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


class HallListView(APIView):
    def get(self, request, stadium_id):
        halls = Hall.objects.filter(stadium_id=stadium_id)
        serializer = HallGetSerializer(halls, many=True)
        response = Response(model=serializer.data, message="The list of halls was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class HallView(APIView):
    def get(self, request, id):
        try:
            hall = Hall.objects.get(id=id)
        except Hall.DoesNotExist:
            response = Response(errors="Hall was not found")
            return JsonResponse(response.to_dict(), status=400)
        serializer = HallGetSerializer(hall)
        response = Response(model=serializer.data, message="Hall info was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)

    def post(self, request):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Hall was created successfully")
            return JsonResponse(response.to_dict(), status=201)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def put(self, request, id):
        try:
            hall = Hall.objects.get(id=id)
        except Hall.DoesNotExist:
            response = Response(errors="Hall was not found")
            return JsonResponse(response.to_dict(), status=400)
        serializer = HallSerializer(hall, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Hall info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def delete(self, request, id):
        try:
            hall = Hall.objects.get(id=id)
        except Hall.DoesNotExist:
            response = Response(errors="Hall was not found")
            return JsonResponse(response.to_dict(), status=400)
        hall.delete()
        response = Response(message="Hall was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class PlaceListView(APIView):
    def get(self, request, hall_id):
        places = Place.objects.filter(hall_id=hall_id).order_by("id")
        page_number = request.query_params.get("pageNumber")
        per_page = request.query_params.get("pageSize")
        paginator = Paginator(places, per_page)
        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)
        serializer = PlaceGetSerializer(page_obj.object_list, many=True)
        response = PageResponse(
            model=serializer.data,
            message="Page of places was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.to_dict(), status=200)


class PlaceView(APIView):
    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Place was created successfully")
            return JsonResponse(response.to_dict(), status=201)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def put(self, request, id):
        try:
            place = Place.objects.get(id=id)
        except Place.DoesNotExist:
            response = Response(errors="Place was not found")
            return JsonResponse(response.to_dict(), status=400)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(model=serializer.data, message="Place info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)
        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def delete(self, request, id):
        try:
            place = Place.objects.get(id=id)
        except Place.DoesNotExist:
            response = Response(errors="Place was not found")
            return JsonResponse(response.to_dict(), status=400)
        place.delete()
        response = Response(message="Place was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class EventAnnouncementView(APIView):
    def get(self, request, city_id):
        now = timezone.now()
        events = Event.objects.filter(hall__stadium__city_id=city_id, start_date__gt=now).order_by('start_date')
        serializer = EventAnnouncementSerializer(events, many=True)
        response = Response(model=serializer.data, message="The list of events was retrieved successfully")
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
