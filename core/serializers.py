from django.contrib.auth.models import Group
from rest_framework import serializers

from core.models import City, User, UserGroupRequest, Stadium


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
