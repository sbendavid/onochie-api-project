# myapp/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer, UserSerializerWithToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import uuid


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def register(request):
    data = request.data
    user_id = str(uuid.uuid4())
    data['user_id'] = user_id
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        user.is_active = True
        user.save()

        # Create organisation
        org_name = f"{user.first_name}'s Organisation"
        org = Organisation.objects.create(org_id=str(uuid.uuid4()), name=org_name)
        org.users.add(user)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': serializer.data
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'errors': serializer.errors
    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'status': 'Bad request',
            'message': 'Email and password are required',
            'statusCode': 400
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    try:
        user = User.objects.get(id=id)
        if user == request.user or request.user.organisations.filter(users=user).exists():
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'status': 'Unauthorized', 'message': 'You do not have permission to view this user'}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return Response({'status': 'Not Found', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    data = request.data
    data['org_id'] = str(uuid.uuid4())
    serializer = OrganisationSerializer(data=data)
    if serializer.is_valid():
        organisation = serializer.save()
        organisation.users.add(request.user)
        return Response({
            'status': 'success',
            'message': 'Organisation created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisations(request):
    organisations = request.user.organisations.all()
    serializer = OrganisationSerializer(organisations, many=True)
    return Response({
        'status': 'success',
        'message': 'Organisations retrieved successfully',
        'data': {'organisations': serializer.data}
    }, status=status.HTTP_200_OK)

