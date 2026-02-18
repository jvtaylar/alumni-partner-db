from django.contrib import admin
from .models import Alumni, Partner, Engagement, Report


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'degree', 'graduation_year', 'status', 'created_at')
    list_filter = ('status', 'degree', 'graduation_year', 'industry')
    search_fields = ('first_name', 'last_name', 'email', 'current_company')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Educational Background', {
            'fields': ('degree', 'field_of_study', 'graduation_year')
        }),
        ('Professional Information', {
            'fields': ('current_company', 'job_title', 'industry')
        }),
        ('Engagement', {
            'fields': ('status', 'linkedin_url', 'bio', 'last_engagement')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'engagement_level', 'primary_contact_name', 'created_at')
    list_filter = ('partner_type', 'engagement_level', 'industry', 'created_at')
    search_fields = ('name', 'email', 'primary_contact_name', 'industry')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Organization Information', {
            'fields': ('name', 'partner_type', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone', 'address', 'city', 'state', 'country')
        }),
        ('Primary Contact', {
            'fields': ('primary_contact_name', 'primary_contact_email', 'primary_contact_phone')
        }),
        ('Engagement Details', {
            'fields': ('engagement_level', 'industry', 'employee_count', 'partnership_start_date', 'last_engagement')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('alumni', 'partner', 'engagement_type', 'engagement_date', 'created_at')
    list_filter = ('engagement_type', 'engagement_date', 'created_at')
    search_fields = ('alumni__first_name', 'alumni__last_name', 'partner__name')
    ordering = ('-engagement_date',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
