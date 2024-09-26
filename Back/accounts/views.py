from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiTypes, extend_schema_view, extend_schema
from rest_framework.views import APIView
from rest_framework import status, mixins, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as django_filters

from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer
from .filters import UserFilter


@extend_schema(
    tags=['Аутентификация'],
    summary="Аутентификация пользователя",
    methods=("POST",),
    description="Аутентификация пользователя",
    request=UserLoginSerializer,
    responses=UserSerializer,
    examples=[
        OpenApiExample(
            "Example 1",
            value={"username": "user", "password": "password"},
            request_only=True,
            response_only=False,
        ),
    ],
)
class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]
    
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)       
        
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({'user_id': user.id,'username': user.username})
        login(request, user) #
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'message': 'Logged in successfully', 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Аутентификация'],
    methods=("POST",),
    summary="Завершение сеанса",
    description="logout",
    request=UserLogoutSerializer,
    examples=[
        OpenApiExample(
            "Example 1",
            value={"refresh": "abracadabra"},
            request_only=True,
            response_only=False,
        ),
    ]
)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        print(request.data)
        refresh_token = request.data.get('refresh') # с клиента нужно отправить refresh token
        
        if not refresh_token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # добавляем токен в черный список
            logout(request)
            return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (django_filters.DjangoFilterBackend, )
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated, ]