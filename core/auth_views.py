from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .auth_serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    AlumniProfileSerializer
)
from .models import Alumni


@api_view(['POST'])
def alumni_register(request):
    """Register a new user account (no alumni profile yet)"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User registration successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'alumni': None,
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def alumni_login(request):
    """Login alumni and return authentication token"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            
            # Get or create alumni profile
            alumni = Alumni.objects.filter(user=user).first()
            
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': UserProfileSerializer(user).data,
                'alumni': AlumniProfileSerializer(alumni).data if alumni else None,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def alumni_logout(request):
    """Logout alumni and delete token"""
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                'error': 'Token not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'error': 'Not authenticated'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def current_user(request):
    """Get current authenticated user details"""
    if request.user.is_authenticated:
        user = request.user
        alumni = Alumni.objects.filter(user=user).first()
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'alumni': AlumniProfileSerializer(alumni).data if alumni else None,
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Not authenticated'
    }, status=status.HTTP_401_UNAUTHORIZED)


class AlumniSelfProfileViewSet(viewsets.ViewSet):
    """ViewSet for alumni to manage their own profile"""
    
    def list(self, request):
        """Get current alumni profile"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            alumni = Alumni.objects.get(user=request.user)
            serializer = AlumniProfileSerializer(alumni)
            return Response(serializer.data)
        except Alumni.DoesNotExist:
            return Response({
                'error': 'Alumni profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """Update alumni profile (partial)"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            alumni = Alumni.objects.get(user=request.user)
            serializer = AlumniProfileSerializer(alumni, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Alumni.DoesNotExist:
            return Response({
                'error': 'Alumni profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Create alumni profile if it doesn't exist"""
        if not request.user.is_authenticated:
            return Response({
                'error': 'Not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if profile already exists
        if Alumni.objects.filter(user=request.user).exists():
            return Response({
                'error': 'Alumni profile already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new alumni profile
        data = request.data.copy()
        
        # Set names from user if not provided
        if 'first_name' not in data or not data['first_name']:
            data['first_name'] = request.user.first_name
        if 'last_name' not in data or not data['last_name']:
            data['last_name'] = request.user.last_name
        if 'email' not in data or not data['email']:
            data['email'] = request.user.email
        
        serializer = AlumniProfileSerializer(data=data)
        if serializer.is_valid():
            alumni = Alumni.objects.create(user=request.user, **data)
            return Response(
                AlumniProfileSerializer(alumni).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
