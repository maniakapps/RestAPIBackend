from abc import ABC
from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serializes data into Company objects"""

    class Meta:
        model = Company
        fields = ('pk', 'name', 'website', 'foundation')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Class used to obtain and serialize data"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    __metaclass__ = ABC

    @classmethod
    def get_token(cls, user) -> Any:
        """Returns a token of the current user"""
        token = TokenObtainPairSerializer.get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """Serializes the register form data"""
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs) -> Any:
        """
        Validates the sttributes
        :param: attrs the form attributes to validate
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data) -> User:
        """Creates a new user
        :param: validated_data the user validated data
        """
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
