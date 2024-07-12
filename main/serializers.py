# myapp/serializers.py
from rest_framework import serializers
from .models import User, Organisation
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone']

class UserSerializerWithToken(UserSerializer):
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'last_name', 'token', 'phone']
        read_only_fields = ['is_active']

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):
        # Explicitly pop the 'confirm_password' field
        validated_data.pop('confirm_password', None)
        # Ensure the 'password' field is processed correctly
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super().create(validated_data)
        return user

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['org_id', 'name', 'description']
