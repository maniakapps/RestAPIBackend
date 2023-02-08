from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serializes data into Company objects"""

    class Meta:
        model = Company
        fields = ('pk', 'name', 'website', 'foundation')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Class used to obtain and serialize data"""

    @classmethod
    def get_token(cls, user) -> dict:
        """Returns a token of the current user"""
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """Serializes the register form data"""
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.HiddenField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs) -> dict:
        """
        Validates the attributes
        :param: attrs the form attributes to validate
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields must match.'})

        password = attrs.pop('password2')
        attrs['email'] = attrs.get('email').lower()
        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data) -> User:
        """Creates a new user"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

