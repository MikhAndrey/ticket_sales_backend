from django.contrib.auth.models import Group
from rest_framework import serializers

from core.models import City, User, UserGroupRequest, Stadium, Hall, Place, Event, Promotion, PromotionEvent


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


class EventAnnouncementSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = PromotionEvent
        fields = "__all__"


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
