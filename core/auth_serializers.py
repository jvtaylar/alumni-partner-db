from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Alumni


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered.'})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'date_joined']


class AlumniProfileSerializer(serializers.ModelSerializer):
    """Serializer for alumni to manage their own profile"""
    user = UserProfileSerializer(read_only=True)
    degree = serializers.CharField()
    field_of_study = serializers.CharField()
    
    class Meta:
        model = Alumni
        fields = [
            'id', 'user',
            'first_name', 'last_name', 'email', 'phone',
            'degree', 'field_of_study', 'graduation_year',
            'current_company', 'job_title', 'industry',
            'status', 'linkedin_url', 'bio',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_field_of_study(self, value):
        allowed = {
            'Civil Engineering',
            'Computer Engineering',
            'Environmental and Sanitary Engineering',
            'Electronics Engineering',
            'Electrical Engineering',
            'Mechanical Engineering',
        }
        if value in allowed:
            return value
        if value and value.strip():
            return value
        raise serializers.ValidationError('Please specify your field of study.')


class AlumniRegistrationSerializer(serializers.Serializer):
    """Serializer for alumni registration (create user and alumni profile)"""
    # User fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    
    # Alumni fields
    phone = serializers.CharField(required=False, allow_blank=True)
    degree = serializers.CharField(max_length=100)
    field_of_study = serializers.CharField(max_length=200)
    graduation_year = serializers.IntegerField()
    current_company = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered.'})
        
        if Alumni.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already has an alumni profile.'})

        return data

    def validate_field_of_study(self, value):
        allowed = {
            'Civil Engineering',
            'Computer Engineering',
            'Environmental and Sanitary Engineering',
            'Electronics Engineering',
            'Electrical Engineering',
            'Mechanical Engineering',
        }
        if value in allowed:
            return value
        if value and value.strip():
            return value
        raise serializers.ValidationError('Please specify your field of study.')
    
    def create(self, validated_data):
        # Extract password2 (not needed for model)
        validated_data.pop('password2')
        
        # Extract alumni-specific fields
        alumni_fields = {
            'phone': validated_data.pop('phone', ''),
            'degree': validated_data.pop('degree'),
            'field_of_study': validated_data.pop('field_of_study'),
            'graduation_year': validated_data.pop('graduation_year'),
            'current_company': validated_data.pop('current_company', ''),
            'job_title': validated_data.pop('job_title', ''),
            'industry': validated_data.pop('industry', ''),
            'linkedin_url': validated_data.pop('linkedin_url', ''),
            'bio': validated_data.pop('bio', ''),
        }
        
        # Create user
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        
        # Create alumni profile
        alumni_fields['user'] = user
        alumni = Alumni.objects.create(**alumni_fields)
        
        return alumni
