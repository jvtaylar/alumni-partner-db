from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from .models import Alumni, Partner, Engagement, Report
import csv
from django.http import HttpResponse


# Audit Trail Model
class AuditLog(admin.ModelAdmin):
    """Base class for models with audit trail"""
    
    def save_model(self, request, obj, form, change):
        if change:
            # Log the change
            changes = []
            for field in form.changed_data:
                changes.append(f"{field}: {form.initial.get(field)} → {form.cleaned_data.get(field)}")
            
            # Create audit log entry in Report model
            Report.objects.create(
                title=f"{obj.__class__.__name__} Updated: {obj}",
                report_type='audit',
                description=f"Modified by {request.user.username}\nChanges: {', '.join(changes)}",
                generated_by=request.user
            )
        else:
            # Log creation
            Report.objects.create(
                title=f"{obj.__class__.__name__} Created: {obj}",
                report_type='audit',
                description=f"Created by {request.user.username}",
                generated_by=request.user
            )
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        # Log deletion
        Report.objects.create(
            title=f"{obj.__class__.__name__} Deleted: {obj}",
            report_type='audit',
            description=f"Deleted by {request.user.username}",
            generated_by=request.user
        )
        super().delete_model(request, obj)


@admin.register(Alumni)
class AlumniAdmin(AuditLog):
    list_display = ('full_name', 'email', 'degree', 'graduation_year', 'status', 'engagement_count', 'last_engagement', 'created_at')
    list_filter = ('status', 'degree', 'graduation_year', 'industry', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'current_company', 'job_title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    list_editable = ('status',)
    actions = ['mark_as_active', 'mark_as_inactive', 'mark_as_lost_contact', 'export_to_csv']
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
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
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    full_name.admin_order_field = 'first_name'
    
    def engagement_count(self, obj):
        count = obj.engagements.count()
        url = reverse('admin:core_engagement_changelist') + f'?alumni__id__exact={obj.id}'
        return format_html('<a href="{}">{} engagements</a>', url, count)
    engagement_count.short_description = 'Engagements'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(engagement_count=Count('engagements'))
    
    # Bulk Actions
    @admin.action(description='Mark selected alumni as Active')
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} alumni marked as active.')
    
    @admin.action(description='Mark selected alumni as Inactive')
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} alumni marked as inactive.')
    
    @admin.action(description='Mark selected alumni as Lost Contact')
    def mark_as_lost_contact(self, request, queryset):
        updated = queryset.update(status='lost_contact')
        self.message_user(request, f'{updated} alumni marked as lost contact.')
    
    @admin.action(description='Export selected alumni to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alumni_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Degree', 'Field of Study', 
                        'Graduation Year', 'Current Company', 'Job Title', 'Industry', 'Status'])
        
        for alumni in queryset:
            writer.writerow([
                alumni.first_name, alumni.last_name, alumni.email, alumni.phone or '',
                alumni.degree, alumni.field_of_study, alumni.graduation_year,
                alumni.current_company, alumni.job_title, alumni.industry, alumni.status
            ])
        
        return response


@admin.register(Partner)
class PartnerAdmin(AuditLog):
    list_display = ('name', 'partner_type', 'engagement_level', 'primary_contact_name', 'engagement_count', 'created_at')
    list_filter = ('partner_type', 'engagement_level', 'industry', 'created_at')
    search_fields = ('name', 'email', 'primary_contact_name', 'industry', 'city', 'country')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    list_editable = ('engagement_level',)
    actions = ['upgrade_to_gold', 'downgrade_to_prospective', 'export_to_csv']
    
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
    
    def engagement_count(self, obj):
        count = obj.engagements.count()
        url = reverse('admin:core_engagement_changelist') + f'?partner__id__exact={obj.id}'
        return format_html('<a href="{}">{} engagements</a>', url, count)
    engagement_count.short_description = 'Engagements'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(engagement_count=Count('engagements'))
    
    # Bulk Actions
    @admin.action(description='Upgrade selected partners to Gold')
    def upgrade_to_gold(self, request, queryset):
        updated = queryset.update(engagement_level='gold')
        self.message_user(request, f'{updated} partners upgraded to Gold level.')
    
    @admin.action(description='Downgrade selected partners to Prospective')
    def downgrade_to_prospective(self, request, queryset):
        updated = queryset.update(engagement_level='prospective')
        self.message_user(request, f'{updated} partners downgraded to Prospective.')
    
    @admin.action(description='Export selected partners to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="partners_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Type', 'Engagement Level', 'Industry', 'Email', 'Phone', 
                        'Primary Contact', 'City', 'Country', 'Partnership Start Date'])
        
        for partner in queryset:
            writer.writerow([
                partner.name, partner.partner_type, partner.engagement_level, partner.industry or '',
                partner.email or '', partner.phone or '', partner.primary_contact_name or '',
                partner.city or '', partner.country or '', partner.partnership_start_date or ''
            ])
        
        return response


@admin.register(Engagement)
class EngagementAdmin(AuditLog):
    list_display = ('alumni_link', 'partner_link', 'engagement_type', 'engagement_date', 'created_by_user', 'created_at')
    list_filter = ('engagement_type', 'engagement_date', 'created_at')
    search_fields = ('alumni__first_name', 'alumni__last_name', 'partner__name', 'description')
    ordering = ('-engagement_date',)
    date_hierarchy = 'engagement_date'
    list_per_page = 50
    actions = ['export_to_csv']
    autocomplete_fields = ['alumni', 'partner']
    
    fieldsets = (
        ('Engagement Details', {
            'fields': ('alumni', 'partner', 'engagement_type', 'engagement_date')
        }),
        ('Description', {
            'fields': ('description', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def alumni_link(self, obj):
        url = reverse('admin:core_alumni_change', args=[obj.alumni.id])
        return format_html('<a href="{}">{}</a>', url, obj.alumni)
    alumni_link.short_description = 'Alumni'
    
    def partner_link(self, obj):
        url = reverse('admin:core_partner_change', args=[obj.partner.id])
        return format_html('<a href="{}">{}</a>', url, obj.partner)
    partner_link.short_description = 'Partner'
    
    def created_by_user(self, obj):
        # Try to find who created this in audit logs
        audit = Report.objects.filter(
            title__contains=f"Engagement Created: {obj}",
            report_type='audit'
        ).first()
        if audit:
            return audit.generated_by.username
        return '-'
    created_by_user.short_description = 'Created By'
    
    @admin.action(description='Export selected engagements to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="engagements_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Alumni', 'Partner', 'Type', 'Date', 'Description', 'Notes'])
        
        for engagement in queryset:
            writer.writerow([
                f"{engagement.alumni.first_name} {engagement.alumni.last_name}",
                engagement.partner.name,
                engagement.get_engagement_type_display(),
                engagement.engagement_date,
                engagement.description,
                engagement.notes
            ])
        
        return response


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'created_at')
    list_filter = ('report_type', 'created_at', 'generated_by')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 100
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'report_type', 'description')
        }),
        ('Generated By', {
            'fields': ('generated_by',)
        }),
        ('Data', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow system to create audit reports
        return False


# Enhanced User Management
class AlumniInline(admin.StackedInline):
    model = Alumni
    can_delete = False
    verbose_name_plural = 'Alumni Profile'
    fk_name = 'user'
    fields = ('first_name', 'last_name', 'email', 'degree', 'graduation_year', 'status')


class CustomUserAdmin(BaseUserAdmin):
    inlines = (AlumniInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    actions = ['activate_users', 'deactivate_users', 'make_staff']
    
    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')
        
        # Log the action
        for user in queryset:
            Report.objects.create(
                title=f"User Activated: {user.username}",
                report_type='audit',
                description=f"Activated by {request.user.username}",
                generated_by=request.user
            )
    
    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
        
        # Log the action
        for user in queryset:
            Report.objects.create(
                title=f"User Deactivated: {user.username}",
                report_type='audit',
                description=f"Deactivated by {request.user.username}",
                generated_by=request.user
            )
    
    @admin.action(description='Grant staff status to selected users')
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} users granted staff status.')
        
        # Log the action
        for user in queryset:
            Report.objects.create(
                title=f"User Granted Staff Status: {user.username}",
                report_type='audit',
                description=f"Modified by {request.user.username}",
                generated_by=request.user
            )


# Unregister the default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site header
admin.site.site_header = "Alumni Partner DB Administration"
admin.site.site_title = "Alumni Partner DB Admin"
admin.site.index_title = "Welcome to Alumni Partner DB Administration"
