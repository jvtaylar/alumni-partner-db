from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Alumni(models.Model):
    """Alumni profile model for tracking alumni information"""
    
    DEGREE_CHOICES = [
        ('BS', 'BS'),
        ('BA', 'BA'),
        ('MS', 'MS'),
        ('MA', 'MA'),
        ('PhD', 'PhD'),
        ('Other', 'Other (Specify)'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lost_contact', 'Lost Contact'),
    ]
    
    # User relationship for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='alumni_profile')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Educational Background
    degree = models.CharField(max_length=120, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=200)
    graduation_year = models.IntegerField()
    
    # Professional Information
    current_company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Contact & Engagement
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    linkedin_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_engagement = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['graduation_year']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Partner(models.Model):
    """Partner organization model for tracking industry and institutional partners"""
    
    PARTNER_TYPE_CHOICES = [
        ('corporate', 'Corporate'),
        ('nonprofit', 'Non-profit'),
        ('government', 'Government'),
        ('educational', 'Educational Institution'),
        ('other', 'Other'),
    ]
    
    ENGAGEMENT_LEVEL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('prospective', 'Prospective'),
    ]
    
    # Organization Information
    name = models.CharField(max_length=255, unique=True)
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Contact Information
    website = models.URLField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Engagement Information
    primary_contact_name = models.CharField(max_length=100, blank=True)
    primary_contact_email = models.EmailField(blank=True)
    primary_contact_phone = models.CharField(max_length=20, blank=True)
    
    engagement_level = models.CharField(
        max_length=20,
        choices=ENGAGEMENT_LEVEL_CHOICES,
        default='prospective'
    )
    
    # Business Details
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.IntegerField(blank=True, null=True)
    partnership_start_date = models.DateField(blank=True, null=True)
    
    # Tracking
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_engagement = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['partner_type']),
            models.Index(fields=['engagement_level']),
        ]
    
    def __str__(self):
        return self.name


class Engagement(models.Model):
    """Engagement tracking between alumni and partners"""
    
    ENGAGEMENT_TYPE_CHOICES = [
        ('networking_event', 'Networking Event'),
        ('mentorship', 'Mentorship'),
        ('interview', 'Interview'),
        ('collaboration', 'Collaboration'),
        ('donation', 'Donation'),
        ('other', 'Other'),
    ]
    
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='engagements')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='engagements')
    
    engagement_type = models.CharField(max_length=50, choices=ENGAGEMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    engagement_date = models.DateTimeField()
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-engagement_date']
        indexes = [
            models.Index(fields=['alumni', 'engagement_date']),
            models.Index(fields=['partner', 'engagement_date']),
        ]
    
    def __str__(self):
        return f"{self.alumni} - {self.partner} ({self.engagement_type})"


class Report(models.Model):
    """Analytics and reporting model"""
    
    REPORT_TYPE_CHOICES = [
        ('alumni_summary', 'Alumni Summary'),
        ('partner_summary', 'Partner Summary'),
        ('engagement_analytics', 'Engagement Analytics'),
        ('retention_analysis', 'Retention Analysis'),
    ]
    
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Report Data (JSON format for flexibility)
    data = models.JSONField(default=dict, blank=True)
    
    generated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_reports'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.report_type})"
