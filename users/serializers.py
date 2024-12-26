from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'phone_number', 'email', 'gender']
        read_only_fields = ['phone_number']
        ref_name = "UserSerializer"


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone_number', 'password']
        ref_name = "UserRegistrationSerializer"

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if not first_name or not first_name.strip():
            raise serializers.ValidationError({"first_name": "First name cannot be empty."})

        if not email or not email.strip():
            raise serializers.ValidationError({"email": "Email cannot be empty."})

        if not phone_number or not phone_number.strip():
            raise serializers.ValidationError({"phone_number": "Phone number cannot be empty."})

        if not password or not password.strip():
            raise serializers.ValidationError({"password": "Password cannot be empty."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "This phone number is already registered."})

        if not phone_number.isdigit() or len(phone_number) > 12:
            raise serializers.ValidationError({
                "phone_number": "Phone number must contain only digits and be at most 12 characters long."
            })

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})

        if not any(char.islower() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})

        special_characters = "@$!%*?&"
        if not any(char in special_characters for char in password):
            raise serializers.ValidationError(
                {"password": f"Password must contain at least one special character: {special_characters}"})

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
