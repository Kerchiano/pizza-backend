from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'email', 'gender']
        read_only_fields = ['phone_number']
        ref_name = "UserSerializer"
