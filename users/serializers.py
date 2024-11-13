from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'phone_number', 'email', 'gender']
        read_only_fields = ['phone_number']
        ref_name = "UserSerializer"


class UserRegistrationSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        ref_name = "UserRegistrationSerializer"

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "This phone number is already registered."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            return data
        except Exception:
            user_exists = User.objects.filter(email=attrs['email']).exists()
            if user_exists:
                raise serializers.ValidationError({"password": "Failed password."})
            else:
                raise serializers.ValidationError({"email": "User with this email does not exist."})
