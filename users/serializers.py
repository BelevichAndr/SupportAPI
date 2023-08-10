from rest_framework import serializers

from users.models import ClientUser, SupportSystemUser


class SupportSystemRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, write_only=True)
    password2 = serializers.CharField(max_length=200)

    class Meta:
        model = SupportSystemUser
        fields = ("email", "password", "first_name",
                  "last_name", "password2")


class ClientUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, write_only=True)
    password2 = serializers.CharField(max_length=200)


    class Meta:
        model = ClientUser
        fields = ("email", "password", "first_name",
                  "last_name", "created_at", "password2")


class SupportSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportSystemUser
        fields = ("pk", "email", "first_name",
                  "last_name", "created_at")


class ClientUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportSystemUser
        fields = ("pk", "email", "first_name",
                  "last_name", "created_at")