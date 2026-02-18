from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import (
    AlumniViewSet, PartnerViewSet, EngagementViewSet, ReportViewSet, 
    landing_page, dashboard_view, alumni_summary_report, analytics_view, 
    alumni_summary_report_pdf, admin_dashboard_view, admin_users_list,
    admin_toggle_user_status, admin_audit_logs, admin_alumni_bulk_action,
    admin_partner_bulk_action, admin_export_data
)
from .auth_views import (
    alumni_register, alumni_login, alumni_logout, current_user,
    AlumniSelfProfileViewSet
)

router = DefaultRouter()
router.register(r'alumni', AlumniViewSet, basename='alumni')
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'engagements', EngagementViewSet, basename='engagement')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'my-profile', AlumniSelfProfileViewSet, basename='my-profile')

urlpatterns = [
    path('', landing_page, name='landing'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('reports/alumni-summary/', alumni_summary_report, name='alumni-summary-report'),
    path('reports/alumni-summary/pdf/', alumni_summary_report_pdf, name='alumni-summary-report-pdf'),
    
    # Admin Dashboard
    path('admin-dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('admin-test/', TemplateView.as_view(template_name='admin-test.html'), name='admin-test'),
    path('token-fix/', TemplateView.as_view(template_name='token-fix.html'), name='token-fix'),
    
    # Web Pages
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('profile/create/', TemplateView.as_view(template_name='profile-create.html'), name='profile-create'),
    path('alumni/', TemplateView.as_view(template_name='alumni-list.html'), name='alumni-list'),
    path('partners/', TemplateView.as_view(template_name='partners-list.html'), name='partners-list'),
    path('engagements/', TemplateView.as_view(template_name='engagements.html'), name='engagements'),
    path('analytics/', analytics_view, name='analytics'),
    
    # Authentication endpoints
    path('auth/register/', alumni_register, name='alumni-register'),
    path('auth/login/', alumni_login, name='alumni-login'),
    path('auth/logout/', alumni_logout, name='alumni-logout'),
    path('auth/user/', current_user, name='current-user'),
    
    # Admin API endpoints
    path('api/admin/users/', admin_users_list, name='admin-users-list'),
    path('api/admin/users/<int:user_id>/toggle-status/', admin_toggle_user_status, name='admin-toggle-user'),
    path('api/admin/audit-logs/', admin_audit_logs, name='admin-audit-logs'),
    path('api/admin/alumni/bulk-action/', admin_alumni_bulk_action, name='admin-alumni-bulk'),
    path('api/admin/partners/bulk-action/', admin_partner_bulk_action, name='admin-partner-bulk'),
    path('api/admin/export/<str:data_type>/', admin_export_data, name='admin-export-data'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
