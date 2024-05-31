import os

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import permission_classes

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from core.helpers import handle_uploaded_file
from core.permissions import CanAddStadium, CanChangeStadium, CanDeleteStadium, CanAddHall, CanChangeHall, \
    CanDeleteHall, \
    CanAddPlace, CanChangePlace, CanDeletePlace, CanAddEvent, CanChangeEvent, CanDeleteEvent, CanAddPromotion, \
    CanChangePromotion, CanDeletePromotion, CanAddPromotionEvent, CanDeletePromotionEvent, CanAddPhoto, CanDeletePhoto
from core.models import City, Stadium, Hall, Place, Event, Promotion, Feedback, PromotionEvent, Photo
from core.response import Response, PageResponse
from core.serializers import CitySerializer, UserRegistrationSerializer, StadiumSerializer, StadiumGetSerializer, \
    HallSerializer, HallGetSerializer, PlaceGetSerializer, PlaceSerializer, EventAnnouncementSerializer, \
    EventGetSerializer, EventSerializer, PromotionSerializer, PromotionGetSerializer, PromotionEventSerializer, \
    FeedbackGetSerializer, FeedbackSerializer, EventPhotoSerializer
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

    @permission_classes([CanAddStadium])
    def post(self, request):
        serializer = StadiumSerializer(data=request.data)
        if serializer.is_valid():
            stadium = serializer.save()
            serializer = StadiumGetSerializer(stadium)
            response = Response(model=serializer.data, message="Stadium was created successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanChangeStadium])
    def put(self, request, id):
        try:
            stadium = Stadium.objects.get(id=id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = StadiumSerializer(stadium, data=request.data)

        if serializer.is_valid():
            stadium = serializer.save()
            serializer = StadiumGetSerializer(stadium)
            response = Response(model=serializer.data, message="Stadium info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeleteStadium])
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


class StadiumPhotoView(APIView):
    @permission_classes([CanAddPhoto])
    def post(self, request):
        try:
            stadium_id = request.query_params['stadium_id']
            stadium = Stadium.objects.get(id=stadium_id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)

        file = request.FILES.get('photo')
        if file:
            file_path = handle_uploaded_file(file, 'stadiums')
            stadium.photo_link = file_path
            stadium.save()

            serializer = StadiumGetSerializer(stadium)
            response = Response(model=serializer.data, message="Stadium photo was added successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors="Photo was not uploaded")
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeletePhoto])
    def delete(self, request, stadium_id):
        try:
            stadium = Stadium.objects.get(id=stadium_id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)

        if stadium.photo_link:
            file_path = os.path.join(settings.MEDIA_ROOT, stadium.photo_link)
            if os.path.exists(file_path):
                os.remove(file_path)
            stadium.photo_link = None
            stadium.save()

        response = Response(message="Stadium photo was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class HallListView(APIView):
    def get(self, request, stadium_id):
        try:
            Stadium.objects.get(id=stadium_id)
        except Stadium.DoesNotExist:
            response = Response(errors="Stadium was not found")
            return JsonResponse(response.to_dict(), status=400)
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

    @permission_classes([CanAddHall])
    def post(self, request):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            hall = serializer.save()
            serializer = HallGetSerializer(hall)
            response = Response(model=serializer.data, message="Hall was created successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanChangeHall])
    def put(self, request, id):
        try:
            hall = Hall.objects.get(id=id)
        except Hall.DoesNotExist:
            response = Response(errors="Hall was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = HallSerializer(hall, data=request.data)
        if serializer.is_valid():
            hall = serializer.save()
            serializer = HallGetSerializer(hall)
            response = Response(model=serializer.data, message="Hall info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeleteHall])
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
    @permission_classes([CanAddPlace])
    def post(self, request):
        place_data = request.data.get('places', [])
        serializer = PlaceSerializer(data=place_data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                places = serializer.save()
                serializer = PlaceGetSerializer(places, many=True)

            response = Response(model=serializer.data, message="Places were added successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanChangePlace])
    def put(self, request):
        place_data = request.data.get('places', [])
        place_ids = [item['id'] for item in place_data]

        try:
            places = Place.objects.filter(id__in=place_ids)
        except Place.DoesNotExist:
            response = Response(errors="One or more places were not found")
            return JsonResponse(response.to_dict(), status=400)

        response_model = []
        with transaction.atomic():
            for i in range(len(places)):
                serializer = PlaceSerializer(places[i], data=place_data[i])
                if serializer.is_valid():
                    place = serializer.save()
                    serializer = PlaceGetSerializer(place)
                    response_model.append(serializer.data)
                else:
                    response = Response(errors=serializer.errors)
                    return JsonResponse(response.to_dict(), status=400)

        response = Response(model=response_model, message="Places were updated successfully")
        return JsonResponse(response.to_dict(), status=200)

    @permission_classes([CanDeletePlace])
    def delete(self, request):
        place_ids = request.data.get('place_ids', [])
        try:
            places = Place.objects.filter(id__in=place_ids)
        except Place.DoesNotExist:
            response = Response(errors="One or more places were not found")
            return JsonResponse(response.to_dict(), status=400)

        with transaction.atomic():
            places.delete()

        response = Response(message="Places were deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class EventView(APIView):
    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)
        serializer = EventGetSerializer(event)

        response = Response(model=serializer.data, message="Event info was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)

    @permission_classes([CanAddEvent])
    def post(self, request):
        data = request.data
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            serializer = EventGetSerializer(event)
            response = Response(model=serializer.data, message="Event was created successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanChangeEvent])
    def put(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            serializer = EventGetSerializer(event)
            response = Response(model=serializer.data, message="Event info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeleteEvent])
    def delete(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)

        photo_link = event.photo_link
        if photo_link:
            file_path = os.path.join(settings.MEDIA_ROOT, photo_link)
            if os.path.exists(file_path):
                os.remove(file_path)
        event.delete()

        response = Response(message="Event was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class EventAnnouncementView(APIView):
    def get(self, request, city_id):
        try:
            City.objects.get(id=city_id)
        except City.DoesNotExist:
            response = Response(errors="City was not found")
            return JsonResponse(response.to_dict(), status=400)
        now = timezone.now()
        events = Event.objects.filter(hall__stadium__city_id=city_id, start_date__gt=now).order_by('start_date')
        serializer = EventAnnouncementSerializer(events, many=True)

        response = Response(model=serializer.data, message="The list of events was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class EventPhotoListView(APIView):
    def get(self, request, event_id):
        try:
            Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)
        photos = Photo.objects.filter(event_id=event_id).order_by('-id')
        serializer = EventPhotoSerializer(photos, many=True)
        response = Response(model=serializer.data, message="The list of event photos was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class EventPhotoView(APIView):
    @permission_classes([CanAddPhoto])
    def post(self, request):
        try:
            event_id = request.query_params['event_id']
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)

        file = request.FILES.get('photo')
        if file:
            file_path = handle_uploaded_file(file, 'events')
            data = {'link': file_path, 'event_id': event_id}
            serializer = EventPhotoSerializer(data=data)

            if serializer.is_valid():
                with transaction.atomic():
                    photo = serializer.save()
                    photos = Photo.objects.filter(event=event)
                    if len(photos) == 1:
                        event.photo_link = photo.link
                        event.save()
                response = Response(model=serializer.data, message="Event photo was added successfully")
                return JsonResponse(response.to_dict(), status=201)

            response = Response(errors=serializer.errors)
            return JsonResponse(response.to_dict(), status=400)

        response = Response(errors="Photo was not uploaded")
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeletePhoto])
    def delete(self, request, id):
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            response = Response(errors="Photo was not found")
            return JsonResponse(response.to_dict(), status=400)

        if photo.link:
            file_path = os.path.join(settings.MEDIA_ROOT, photo.link)
            if os.path.exists(file_path):
                os.remove(file_path)

        event = Event.objects.get(id=photo.event_id)
        with transaction.atomic():
            photo.delete()
            photos = Photo.objects.filter(event=event)
            if len(photos) == 0:
                event.photo_link = None
                event.save()

        response = Response(message="Event photo was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class PromotionView(APIView):
    def get(self, request, id):
        try:
            promotion = Promotion.objects.get(id=id)
        except Promotion.DoesNotExist:
            response = Response(errors="Promotion was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = PromotionGetSerializer(promotion)

        response = Response(model=serializer.data, message="Promotion info was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)

    @permission_classes([CanAddPromotion])
    def post(self, request):
        data = request.data
        serializer = PromotionSerializer(data={
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "discount": data["discount"]})
        if serializer.is_valid():
            with transaction.atomic():
                promotion = serializer.save()
                event_ids = data["event_ids"]
                try:
                    events = Event.objects.filter(id__in=event_ids)
                    for event in events:
                        promotion_event_serializer = PromotionEventSerializer(data={
                            "event": event.id,
                            "promotion": promotion.id
                        })
                        if promotion_event_serializer.is_valid():
                            promotion_event_serializer.save()
                        else:
                            response = Response(errors=promotion_event_serializer.errors)
                            return JsonResponse(response.to_dict(), status=400)

                except Event.DoesNotExist:
                    response = Response(errors="One or more events were not found")
                    return JsonResponse(response.to_dict(), status=400)

            serializer = PromotionGetSerializer(promotion)

            response = Response(model=serializer.data, message="Promotion was created successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanChangePromotion])
    def put(self, request, id):
        try:
            promotion = Promotion.objects.get(id=id)
        except Promotion.DoesNotExist:
            response = Response(errors="Promotion was not found")
            return JsonResponse(response.to_dict(), status=400)

        data = request.data
        serializer = PromotionSerializer(promotion, data={
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "discount": data["discount"]})

        if serializer.is_valid():
            promotion = serializer.save()
            serializer = PromotionGetSerializer(promotion)
            response = Response(model=serializer.data, message="Promotion was updated successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeletePromotion])
    def delete(self, request, id):
        try:
            promotion = Promotion.objects.get(id=id)
        except Promotion.DoesNotExist:
            response = Response(errors="Promotion was not found")
            return JsonResponse(response.to_dict(), status=400)

        promotion.delete()

        response = Response(message="Promotion was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class PromotionEventView(APIView):
    @permission_classes([CanAddPromotionEvent])
    def post(self, request):
        serializer = PromotionEventSerializer(data=request.data)
        if serializer.is_valid():
            promotion_event = serializer.save()
            serializer = PromotionGetSerializer(promotion_event.promotion)

            response = Response(model=serializer.data, message="Promotion for event was added successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    @permission_classes([CanDeletePromotionEvent])
    def delete(self, request):
        try:
            promotion_event = PromotionEvent.objects.get(
                event_id=request.query_params["event_id"],
                promotion_id=request.query_params["promotion_id"])
        except PromotionEvent.DoesNotExist:
            response = Response(errors="Promotion for this event was not found")
            return JsonResponse(response.to_dict(), status=400)

        promotion_event.delete()

        response = Response(message="Promotion for specified event was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class FeedbackListView(APIView):
    def get(self, request, event_id):
        try:
            Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            response = Response(errors="Event was not found")
            return JsonResponse(response.to_dict(), status=400)
        feedbacks = Feedback.objects.filter(event_id=event_id).order_by('-date')
        serializer = FeedbackGetSerializer(feedbacks, many=True)
        response = Response(model=serializer.data, message="The list of feedbacks was retrieved successfully")
        return JsonResponse(response.to_dict(), status=200)


class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save(user=request.user, date=timezone.now())
            serializer = FeedbackGetSerializer(feedback)
            response = Response(model=serializer.data, message="Feedback was created successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def put(self, request, id):
        try:
            feedback = Feedback.objects.get(id=id)
        except Feedback.DoesNotExist:
            response = Response(errors="Feedback was not found")
            return JsonResponse(response.to_dict(), status=400)

        serializer = FeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            serializer = FeedbackGetSerializer(feedback)
            response = Response(model=serializer.data, message="Feedback info was updated successfully")
            return JsonResponse(response.to_dict(), status=200)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)

    def delete(self, request, id):
        try:
            feedback = Feedback.objects.get(id=id)
        except Feedback.DoesNotExist:
            response = Response(errors="Feedback was not found")
            return JsonResponse(response.to_dict(), status=400)
        feedback.delete()

        response = Response(message="Feedback was deleted successfully")
        return JsonResponse(response.to_dict(), status=204)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(message="The user was registered successfully")
            return JsonResponse(response.to_dict(), status=201)

        response = Response(errors=serializer.errors)
        return JsonResponse(response.to_dict(), status=400)
