from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import AlumniViewSet, PartnerViewSet, EngagementViewSet, ReportViewSet, landing_page, dashboard_view
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
    
    # Web Pages
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('profile/create/', TemplateView.as_view(template_name='profile-create.html'), name='profile-create'),
    path('alumni/', TemplateView.as_view(template_name='alumni-list.html'), name='alumni-list'),
    path('partners/', TemplateView.as_view(template_name='partners-list.html'), name='partners-list'),
    path('engagements/', TemplateView.as_view(template_name='engagements.html'), name='engagements'),
    path('analytics/', TemplateView.as_view(template_name='analytics.html'), name='analytics'),
    
    # Authentication endpoints
    path('auth/register/', alumni_register, name='alumni-register'),
    path('auth/login/', alumni_login, name='alumni-login'),
    path('auth/logout/', alumni_logout, name='alumni-logout'),
    path('auth/user/', current_user, name='current-user'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
