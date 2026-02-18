from rest_framework import serializers
from .models import Alumni, Partner, Engagement, Report


class AlumniSerializer(serializers.ModelSerializer):
    """Serializer for Alumni model"""
    degree = serializers.CharField()
    
    class Meta:
        model = Alumni
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'degree', 'field_of_study', 'graduation_year',
            'current_company', 'job_title', 'industry',
            'status', 'linkedin_url', 'bio',
            'created_at', 'updated_at', 'last_engagement'
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


class AlumniDetailSerializer(AlumniSerializer):
    """Detailed serializer for Alumni including engagements"""
    engagements = serializers.SerializerMethodField()
    
    class Meta(AlumniSerializer.Meta):
        fields = AlumniSerializer.Meta.fields + ['engagements']
    
    def get_engagements(self, obj):
        engagements = obj.engagements.all()
        return EngagementSerializer(engagements, many=True).data


class PartnerSerializer(serializers.ModelSerializer):
    """Serializer for Partner model"""
    
    class Meta:
        model = Partner
        fields = [
            'id', 'name', 'partner_type', 'description',
            'website', 'email', 'phone', 'address', 'city', 'state', 'country',
            'primary_contact_name', 'primary_contact_email', 'primary_contact_phone',
            'engagement_level', 'industry', 'employee_count', 'partnership_start_date',
            'notes', 'created_at', 'updated_at', 'last_engagement'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PartnerDetailSerializer(PartnerSerializer):
    """Detailed serializer for Partner including engagements"""
    engagements = serializers.SerializerMethodField()
    engagement_count = serializers.SerializerMethodField()
    
    class Meta(PartnerSerializer.Meta):
        fields = PartnerSerializer.Meta.fields + ['engagements', 'engagement_count']
    
    def get_engagements(self, obj):
        engagements = obj.engagements.all()[:10]  # Last 10 engagements
        return EngagementSerializer(engagements, many=True).data
    
    def get_engagement_count(self, obj):
        return obj.engagements.count()


class EngagementSerializer(serializers.ModelSerializer):
    """Serializer for Engagement model"""
    alumni_name = serializers.CharField(source='alumni.__str__', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    
    class Meta:
        model = Engagement
        fields = [
            'id', 'alumni', 'alumni_name', 'partner', 'partner_name',
            'engagement_type', 'description', 'engagement_date',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model"""
    generated_by_name = serializers.CharField(source='generated_by.username', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'title', 'report_type', 'description',
            'data', 'generated_by', 'generated_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AlumniStatsSerializer(serializers.Serializer):
    """Serializer for alumni statistics"""
    total_alumni = serializers.IntegerField()
    active_alumni = serializers.IntegerField()
    by_degree = serializers.DictField()
    by_graduation_year = serializers.DictField()
    by_industry = serializers.DictField()


class PartnerStatsSerializer(serializers.Serializer):
    """Serializer for partner statistics"""
    total_partners = serializers.IntegerField()
    by_type = serializers.DictField()
    by_engagement_level = serializers.DictField()
    by_industry = serializers.DictField()
