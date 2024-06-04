from django.contrib.auth.models import Group
from rest_framework import serializers

from core.models import City, User, UserGroupRequest, Stadium, Hall, Place, Event, Promotion, PromotionEvent, Feedback, \
    Photo, Video, EventRequest, EventRequestPlace, EventPlace, Purchase


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StadiumGetSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = Stadium
        fields = ['id', 'address', 'name', 'description', 'photo_link', 'contacts', 'city']

    def get_city(self, obj: Stadium):
        return {
            "id": obj.city.id,
            "name": obj.city.name
        }


class StadiumSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(source='city', queryset=City.objects.all())
    city_id.default_error_messages['does_not_exist'] = 'City was not found'

    class Meta:
        model = Stadium
        fields = ['id', 'address', 'name', 'description', 'photo_link', 'contacts', 'city_id']


class HallGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    stadium_id = serializers.PrimaryKeyRelatedField(source='stadium', queryset=Stadium.objects.all())
    stadium_id.default_error_messages['does_not_exist'] = 'Stadium was not found'

    class Meta:
        model = Hall
        fields = ['id', 'name', 'stadium_id']


class PlaceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    hall_id = serializers.PrimaryKeyRelatedField(source='hall', queryset=Hall.objects.all())
    hall_id.default_error_messages['does_not_exist'] = 'Hall was not found'

    class Meta:
        model = Place
        fields = ['id', 'sector', 'row', 'seat', 'x_offset', 'y_offset', 'hall_id']


class EventListSerializer(serializers.ModelSerializer):
    hall = serializers.SerializerMethodField()
    stadium = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_hall(self, obj: Event):
        return {
            "id": obj.hall.id,
            "name": obj.hall.name
        }

    def get_stadium(self, obj: Event):
        return {
            "id": obj.hall.stadium.id,
            "name": obj.hall.stadium.name
        }


class EventGetSerializer(serializers.ModelSerializer):
    hall = serializers.SerializerMethodField()
    stadium = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'photo_link', 'contacts', 'hall', 'stadium']

    def get_hall(self, obj: Event):
        return {
            "id": obj.hall.id,
            "name": obj.hall.name
        }

    def get_stadium(self, obj: Event):
        return {
            "id": obj.hall.stadium.id,
            "name": obj.hall.stadium.name
        }


class EventSerializer(serializers.ModelSerializer):
    hall_id = serializers.PrimaryKeyRelatedField(source='hall', queryset=Hall.objects.all())
    hall_id.default_error_messages['does_not_exist'] = 'Hall was not found'

    class Meta:
        model = Event
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'contacts', 'hall_id']


class EventPhotoSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(source='event', queryset=Event.objects.all())
    event_id.default_error_messages['does_not_exist'] = 'Event was not found'

    class Meta:
        model = Photo
        fields = ['id', 'link', 'event_id']


class EventVideoSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(source='event', queryset=Event.objects.all())
    event_id.default_error_messages['does_not_exist'] = 'Event was not found'

    class Meta:
        model = Video
        fields = ['id', 'link', 'event_id']


class EventRequestPlaceSerializer(serializers.ModelSerializer):
    place_id = serializers.PrimaryKeyRelatedField(source='place', queryset=Place.objects.all())
    place_id.default_error_messages['does_not_exist'] = 'Place was not found'

    class Meta:
        model = EventRequestPlace
        fields = ['place_id', 'price']


class EventPlaceGetSerializer(serializers.ModelSerializer):
    purchase = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    class Meta:
        model = EventPlace
        fields = ['id', 'place', 'discounted_price', 'purchase']

    def get_place(self, obj: EventPlace):
        return PlaceGetSerializer(obj.place).data

    def get_purchase(self, obj: EventPlace):
        return PurchaseGetSerializer(obj.purchase).data


class EventPlaceDetailsSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventPlace
        fields = ['id', 'place', 'discounted_price', 'event']

    def get_place(self, obj: EventPlace):
        return PlaceGetSerializer(obj.place).data

    def get_event(self, obj: EventPlace):
        return EventGetSerializer(obj.event).data


class PurchaseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'date', 'status']


class PurchaseDetailsSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['id', 'date', 'status', 'places']

    def get_places(self, obj: Purchase):
        places = EventPlace.objects.filter(purchase=obj)
        return EventPlaceDetailsSerializer(places, many=True).data


class EventRequestPlaceGetSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()

    class Meta:
        model = EventRequestPlace
        fields = ['id', 'place', 'price']

    def get_place(self, obj: EventRequestPlace):
        return PlaceGetSerializer(obj.place).data


class EventRequestCreateSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(source='event', queryset=Event.objects.all())
    event_id.default_error_messages['does_not_exist'] = 'Event was not found'

    places = EventRequestPlaceSerializer(many=True)

    class Meta:
        model = EventRequest
        fields = ['event_id', 'places']

    def create(self, validated_data):
        places_data = validated_data.pop('places')
        event_request = EventRequest.objects.create(**validated_data)
        for place_data in places_data:
            place_data['event_request'] = event_request
            EventRequestPlace.objects.create(**place_data)
        return event_request


class EventRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRequest
        fields = ['id', 'status']

    def update(self, instance, validated_data):
        previous_status = instance.status
        if previous_status != 'in_review':
            raise serializers.ValidationError("This request has already been approved or rejected")

        instance = super().update(instance, validated_data)

        if previous_status != 'approved' and instance.status == 'approved':
            event_request_places = EventRequestPlace.objects.filter(event_request_id=instance.id)
            for request_place in event_request_places:
                EventPlace.objects.create(
                    event=instance.event,
                    place=request_place.place,
                    price=request_place.price,
                    purchase=None
                )

        return instance


class EventRequestDetailsSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventRequest
        fields = ['id', 'status', 'event', 'places']

    def get_event(self, obj: EventRequest):
        return {
            'id': obj.event_id,
            'name': obj.event.name,
        }

    def get_places(self, obj: EventRequest):
        places = EventRequestPlace.objects.filter(event_request=obj)
        return EventRequestPlaceGetSerializer(places, many=True).data


class EventRequestGetSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventRequest
        fields = ['id', 'status', 'event']

    def get_event(self, obj: EventRequest):
        return {
            'id': obj.event_id,
            'name': obj.event.name,
        }


class EventRequestStadiumGetSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    hall = serializers.SerializerMethodField()
    stadium = serializers.SerializerMethodField()

    class Meta:
        model = EventRequest
        fields = ['id', 'status', 'event', 'hall', 'stadium']

    def get_event(self, obj: EventRequest):
        return {
            'id': obj.event_id,
            'name': obj.event.name,
        }

    def get_hall(self, obj: EventRequest):
        return {
            'id': obj.event.hall.id,
            'name': obj.event.hall.name,
        }

    def get_stadium(self, obj: EventRequest):
        return {
            'id': obj.event.hall.stadium.id,
            'name': obj.event.hall.stadium.name,
        }


class EventRequestPlaceCreateSerializer(serializers.ModelSerializer):
    place_id = serializers.PrimaryKeyRelatedField(source='place', queryset=Place.objects.all())
    place_id.default_error_messages['does_not_exist'] = 'Place was not found'

    class Meta:
        model = EventRequestPlace
        fields = ['place_id', 'price']


class PromotionGetSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['start_date', 'end_date', 'discount', 'events']

    def get_events(self, obj: Promotion):
        promotion_events = PromotionEvent.objects.filter(promotion=obj)
        return EventGetSerializer([pe.event for pe in promotion_events], many=True).data


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"


class PromotionEventSerializer(serializers.ModelSerializer):
    promotion_id = serializers.PrimaryKeyRelatedField(source='promotion', queryset=Promotion.objects.all())
    promotion_id.default_error_messages['does_not_exist'] = 'Promotion was not found'

    event_id = serializers.PrimaryKeyRelatedField(source='event', queryset=Event.objects.all())
    event_id.default_error_messages['does_not_exist'] = 'Event was not found'

    class Meta:
        model = PromotionEvent
        fields = ["promotion_id", "event_id"]

    def validate(self, data):
        event = Event.objects.get(id=data['event_id'])
        if event.user != self.context['request'].user:
            raise serializers.ValidationError("You can add a promotion only for your events")
        return data


class FeedbackGetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'text', 'date', 'mark', 'user']

    def get_user(self, obj: Feedback):
        return {
            "id": obj.user.id,
            "name": obj.user.login
        }


class FeedbackSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(source='event', queryset=Event.objects.all())
    event_id.default_error_messages['does_not_exist'] = 'Event was not found'

    class Meta:
        model = Feedback
        fields = ['id', 'text', 'mark', 'event_id']

    def validate(self, data):
        if not EventPlace.objects.filter(event_id=data['event_id'], purchase__user=self.context['user']).exists():
            raise serializers.ValidationError("You need to buy tickets for this event before leaving a feedback")
        return data


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    requested_groups = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True
    )

    class Meta:
        model = User
        fields = ('login', 'password', 'password_confirm', 'requested_groups')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        requested_groups = validated_data.pop('requested_groups', [])
        user = User.objects.create_user(**validated_data)

        for group_name in requested_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            UserGroupRequest.objects.create(user=user, group=group)

        return user
