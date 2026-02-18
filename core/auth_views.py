from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .auth_serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    AlumniProfileSerializer
)
from .models import Alumni


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def alumni_login(request):
    """Login alumni and return authentication token"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username'].strip()
        password = serializer.validated_data['password']
        
        # Allow login with email or username
        user = authenticate(username=username, password=password)
        if user is None:
            try:
                username_user = User.objects.get(username__iexact=username)
                user = authenticate(username=username_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None and '@' in username:
            try:
                email_user = User.objects.get(email__iexact=username)
                user = authenticate(username=email_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            password_trimmed = password.strip()
            if password_trimmed:
                try:
                    fallback_user = User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    fallback_user = None

                if fallback_user is None and '@' in username:
                    try:
                        fallback_user = User.objects.get(email__iexact=username)
                    except User.DoesNotExist:
                        fallback_user = None

                if fallback_user and fallback_user.is_active and fallback_user.check_password(password_trimmed):
                    user = fallback_user
        
        if user is not None:
            login(request, user)
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
@permission_classes([AllowAny])
def alumni_logout(request):
    """Logout alumni and delete token"""
    if request.user.is_authenticated:
        logout(request)

    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_user(request):
    """Get current authenticated user details"""
    # Resolve user with token auth taking priority over session
    user = request.user
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Token '):
        token_key = auth_header.split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            user = None

    if user is not None and user.is_authenticated:
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
        # Remove csrf token if present (from form submissions)
        if 'csrfmiddlewaretoken' in data:
            data.pop('csrfmiddlewaretoken')
        
        # Set names from user if not provided
        if 'first_name' not in data or not data['first_name']:
            data['first_name'] = request.user.first_name
        if 'last_name' not in data or not data['last_name']:
            data['last_name'] = request.user.last_name
        if 'email' not in data or not data['email']:
            data['email'] = request.user.email
        
        serializer = AlumniProfileSerializer(data=data)
        if serializer.is_valid():
            alumni = Alumni.objects.create(user=request.user, **serializer.validated_data)
            return Response(
                AlumniProfileSerializer(alumni).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update current user's basic profile fields"""
    user = request.user
    data = request.data.copy()

    # Only allow specific fields
    allowed_fields = {'first_name', 'last_name', 'email', 'username'}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if 'email' in update_data:
        email = update_data['email'].strip()
        if User.objects.exclude(id=user.id).filter(email__iexact=email).exists():
            return Response({'email': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        update_data['email'] = email

    if 'username' in update_data:
        username = update_data['username'].strip()
        if User.objects.exclude(id=user.id).filter(username__iexact=username).exists():
            return Response({'username': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        update_data['username'] = username

    for field, value in update_data.items():
        setattr(user, field, value)
    user.save()

    return Response({'user': UserProfileSerializer(user).data}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_alumni_profile(request):
    """Update current user's alumni profile"""
    try:
        alumni = Alumni.objects.get(user=request.user)
    except Alumni.DoesNotExist:
        return Response({'error': 'Alumni profile not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    if 'csrfmiddlewaretoken' in data:
        data.pop('csrfmiddlewaretoken')

    serializer = AlumniProfileSerializer(alumni, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change current user's password"""
    user = request.user
    old_password = request.data.get('old_password', '')
    new_password = request.data.get('new_password', '')
    new_password2 = request.data.get('new_password2', '')

    if not user.check_password(old_password):
        return Response({'old_password': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password or new_password != new_password2:
        return Response({'new_password': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
