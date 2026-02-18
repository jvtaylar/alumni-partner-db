from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Alumni, Partner, Engagement, Report
from .serializers import (
    AlumniSerializer, AlumniDetailSerializer,
    PartnerSerializer, PartnerDetailSerializer,
    EngagementSerializer, ReportSerializer,
    AlumniStatsSerializer, PartnerStatsSerializer
)
import io
from django.http import HttpResponse
from django.utils import timezone

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


def _create_pdf_bytes(title, data_lines):
    """Create a simple PDF in-memory from title and list of text lines.

    Returns bytes of PDF. Requires reportlab.
    """
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 72
    c.setFont('Helvetica-Bold', 16)
    c.drawString(72, y, title)
    y -= 28
    c.setFont('Helvetica', 10)
    for line in data_lines:
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont('Helvetica', 10)
        c.drawString(72, y, line)
        y -= 14

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def _report_lines(report):
    """Convert a Report object into a list of text lines for PDF output."""
    data = report.data or {}

    if report.report_type == 'alumni_summary':
        lines = [
            f"Total alumni: {data.get('total_alumni', 0)}",
            f"Active alumni: {data.get('active_alumni', 0)}",
            f"Inactive alumni: {data.get('inactive_alumni', 0)}",
            "",
            "By degree:",
        ]
        for deg, cnt in (data.get('by_degree') or {}).items():
            lines.append(f"- {deg}: {cnt}")
        return lines

    if report.report_type == 'partner_summary':
        lines = [
            f"Total partners: {data.get('total_partners', 0)}",
            "",
            "By type:",
        ]
        for t, cnt in (data.get('by_type') or {}).items():
            lines.append(f"- {t}: {cnt}")
        lines.append("")
        lines.append("By engagement level:")
        for lvl, cnt in (data.get('by_engagement_level') or {}).items():
            lines.append(f"- {lvl}: {cnt}")
        return lines

    if report.report_type == 'engagement_analytics':
        lines = [
            f"Total engagements: {data.get('total_engagements', 0)}",
            "",
            "By type:",
        ]
        for t, cnt in (data.get('by_type') or {}).items():
            lines.append(f"- {t}: {cnt}")
        lines.append("")
        lines.append("Top partners:")
        for p in (data.get('top_partners') or []):
            lines.append(f"- {p.get('name')}: {p.get('count')}")
        return lines

    # Fallback
    return ["Report data:", str(data)]


def landing_page(request):
    """Landing page view with statistics"""
    alumni_count = Alumni.objects.count()
    partner_count = Partner.objects.count()
    engagement_count = Engagement.objects.count()
    
    context = {
        'alumni_count': alumni_count,
        'partner_count': partner_count,
        'engagement_count': engagement_count,
    }
    return render(request, 'index.html', context)


def dashboard_view(request):
    """Dashboard view for authenticated users"""
    # Check if user has token in localStorage (from API login)
    # If not authenticated via session, show login page
    if not request.user.is_authenticated:
        # Check if coming from API login with token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Token '):
            # Render dashboard but let frontend JS handle auth check
            pass
    
    alumni = None
    if request.user.is_authenticated:
        alumni = Alumni.objects.filter(user=request.user).first()
    
    alumni_count = Alumni.objects.count()
    partner_count = Partner.objects.count()
    engagement_count = Engagement.objects.count()
    
    context = {
        'alumni': alumni,
        'alumni_count': alumni_count,
        'partner_count': partner_count,
        'engagement_count': engagement_count,
    }
    return render(request, 'dashboard.html', context)


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AlumniViewSet(viewsets.ModelViewSet):
    """ViewSet for Alumni management"""
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'degree', 'graduation_year', 'industry']
    search_fields = ['first_name', 'last_name', 'email', 'current_company']
    ordering_fields = ['created_at', 'graduation_year', 'last_engagement']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlumniDetailSerializer
        return AlumniSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get alumni statistics and analytics"""
        total = Alumni.objects.count()
        active = Alumni.objects.filter(status='active').count()
        
        # By degree
        by_degree = dict(
            Alumni.objects.values_list('degree').annotate(
                count=Count('id')
            )
        )
        
        # By graduation year
        by_year = dict(
            Alumni.objects.values_list('graduation_year').annotate(
                count=Count('id')
            )
        )
        
        # By industry
        by_industry = dict(
            Alumni.objects.filter(industry__isnull=False).exclude(industry='')
            .values_list('industry').annotate(count=Count('id'))
        )
        
        data = {
            'total_alumni': total,
            'active_alumni': active,
            'by_degree': by_degree,
            'by_graduation_year': by_year,
            'by_industry': by_industry,
        }
        
        serializer = AlumniStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_company(self, request):
        """Search alumni by company"""
        company = request.query_params.get('company', '')
        if not company:
            return Response({'error': 'company parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Alumni.objects.filter(current_company__icontains=company)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def record_engagement(self, request, pk=None):
        """Record engagement with partner"""
        alumni = self.get_object()
        partner_id = request.data.get('partner_id')
        engagement_type = request.data.get('engagement_type')
        engagement_date = request.data.get('engagement_date')
        
        if not all([partner_id, engagement_type, engagement_date]):
            return Response(
                {'error': 'partner_id, engagement_type, and engagement_date required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            partner = Partner.objects.get(id=partner_id)
            engagement = Engagement.objects.create(
                alumni=alumni,
                partner=partner,
                engagement_type=engagement_type,
                engagement_date=engagement_date,
                description=request.data.get('description', '')
            )
            serializer = EngagementSerializer(engagement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Partner.DoesNotExist:
            return Response({'error': 'Partner not found'}, status=status.HTTP_404_NOT_FOUND)


class PartnerViewSet(viewsets.ModelViewSet):
    """ViewSet for Partner management"""
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['partner_type', 'engagement_level', 'industry']
    search_fields = ['name', 'email', 'primary_contact_name', 'industry']
    ordering_fields = ['created_at', 'engagement_level', 'last_engagement']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartnerDetailSerializer
        return PartnerSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get partner statistics and analytics"""
        total = Partner.objects.count()
        
        # By partner type
        by_type = dict(
            Partner.objects.values_list('partner_type').annotate(
                count=Count('id')
            )
        )
        
        # By engagement level
        by_level = dict(
            Partner.objects.values_list('engagement_level').annotate(
                count=Count('id')
            )
        )
        
        # By industry
        by_industry = dict(
            Partner.objects.filter(industry__isnull=False).exclude(industry='')
            .values_list('industry').annotate(count=Count('id'))
        )
        
        data = {
            'total_partners': total,
            'by_type': by_type,
            'by_engagement_level': by_level,
            'by_industry': by_industry,
        }
        
        serializer = PartnerStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_engaged(self, request):
        """Get top engaged partners"""
        limit = int(request.query_params.get('limit', 10))
        partners = Partner.objects.annotate(
            engagement_count=Count('engagements')
        ).order_by('-engagement_count')[:limit]
        
        serializer = self.get_serializer(partners, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def record_engagement(self, request, pk=None):
        """Record engagement with alumni"""
        partner = self.get_object()
        alumni_id = request.data.get('alumni_id')
        engagement_type = request.data.get('engagement_type')
        engagement_date = request.data.get('engagement_date')
        
        if not all([alumni_id, engagement_type, engagement_date]):
            return Response(
                {'error': 'alumni_id, engagement_type, and engagement_date required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            alumni = Alumni.objects.get(id=alumni_id)
            engagement = Engagement.objects.create(
                alumni=alumni,
                partner=partner,
                engagement_type=engagement_type,
                engagement_date=engagement_date,
                description=request.data.get('description', '')
            )
            serializer = EngagementSerializer(engagement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Alumni.DoesNotExist:
            return Response({'error': 'Alumni not found'}, status=status.HTTP_404_NOT_FOUND)


class EngagementViewSet(viewsets.ModelViewSet):
    """ViewSet for Engagement management"""
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['alumni', 'partner', 'engagement_type']
    search_fields = ['alumni__first_name', 'alumni__last_name', 'partner__name']
    ordering_fields = ['engagement_date', 'created_at']
    ordering = ['-engagement_date']
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get engagements by type"""
        engagement_type = request.query_params.get('type')
        if not engagement_type:
            return Response({'error': 'type parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        engagements = Engagement.objects.filter(engagement_type=engagement_type)
        serializer = self.get_serializer(engagements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent engagements"""
        limit = int(request.query_params.get('limit', 20))
        recent = Engagement.objects.all()[:limit]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Report management"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['report_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the generated_by user when creating a report"""
        serializer.save(generated_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_alumni_summary(self, request):
        """Generate alumni summary report"""
        total = Alumni.objects.count()
        active = Alumni.objects.filter(status='active').count()
        by_degree = dict(
            Alumni.objects.values_list('degree').annotate(count=Count('id'))
        )
        
        data = {
            'total_alumni': total,
            'active_alumni': active,
            'inactive_alumni': total - active,
            'by_degree': by_degree,
        }
        
        report = Report.objects.create(
            title='Alumni Summary Report',
            report_type='alumni_summary',
            data=data,
            generated_by=request.user
        )
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def generate_partner_summary(self, request):
        """Generate partner summary report"""
        total = Partner.objects.count()
        by_type = dict(
            Partner.objects.values_list('partner_type').annotate(count=Count('id'))
        )
        by_level = dict(
            Partner.objects.values_list('engagement_level').annotate(count=Count('id'))
        )
        
        data = {
            'total_partners': total,
            'by_type': by_type,
            'by_engagement_level': by_level,
        }
        
        report = Report.objects.create(
            title='Partner Summary Report',
            report_type='partner_summary',
            data=data,
            generated_by=request.user
        )
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def generate_engagement_analytics(self, request):
        """Generate engagement analytics report"""
        total_engagements = Engagement.objects.count()
        by_type = dict(
            Engagement.objects.values_list('engagement_type').annotate(count=Count('id'))
        )

        # Top partners by engagements
        top_partners_qs = Partner.objects.annotate(engagement_count=Count('engagements')).order_by('-engagement_count')[:10]
        top_partners = [{ 'name': p.name, 'count': p.engagement_count } for p in top_partners_qs]

        data = {
            'total_engagements': total_engagements,
            'by_type': by_type,
            'top_partners': top_partners,
        }

        report = Report.objects.create(
            title='Engagement Analytics Report',
            report_type='engagement_analytics',
            data=data,
            generated_by=request.user
        )
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Render a simple HTML preview for a report"""
        report = self.get_object()
        context = {
            'report': report,
            'generated_at': report.created_at or timezone.now(),
        }
        return render(request, 'report_preview.html', context)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Download a PDF for an existing report"""
        report = self.get_object()

        if not REPORTLAB_AVAILABLE:
            return Response({'error': 'reportlab not installed on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lines = _report_lines(report)
        pdf = _create_pdf_bytes(report.title, lines)
        if pdf is None:
            return Response({'error': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resp = HttpResponse(pdf, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'
        return resp

    @action(detail=False, methods=['post'])
    def generate_alumni_summary_pdf(self, request):
        """Generate alumni summary report and return PDF"""
        # Build same data
        total = Alumni.objects.count()
        active = Alumni.objects.filter(status='active').count()
        by_degree = dict(
            Alumni.objects.values_list('degree').annotate(count=Count('id'))
        )

        data = {
            'total_alumni': total,
            'active_alumni': active,
            'inactive_alumni': total - active,
            'by_degree': by_degree,
        }

        report = Report.objects.create(
            title='Alumni Summary Report',
            report_type='alumni_summary',
            data=data,
            generated_by=request.user
        )

        # Create PDF
        if not REPORTLAB_AVAILABLE:
            return Response({'error': 'reportlab not installed on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lines = [f"Total alumni: {data['total_alumni']}", f"Active alumni: {data['active_alumni']}", f"Inactive alumni: {data['inactive_alumni']}", "", 'By degree:']
        for deg, cnt in data['by_degree'].items():
            lines.append(f"- {deg}: {cnt}")

        pdf = _create_pdf_bytes(report.title, lines)
        if pdf is None:
            return Response({'error': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resp = HttpResponse(pdf, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="report_{report.id}_alumni.pdf"'
        return resp

    @action(detail=False, methods=['post'])
    def generate_partner_summary_pdf(self, request):
        """Generate partner summary report and return PDF"""
        total = Partner.objects.count()
        by_type = dict(
            Partner.objects.values_list('partner_type').annotate(count=Count('id'))
        )
        by_level = dict(
            Partner.objects.values_list('engagement_level').annotate(count=Count('id'))
        )

        data = {
            'total_partners': total,
            'by_type': by_type,
            'by_engagement_level': by_level,
        }

        report = Report.objects.create(
            title='Partner Summary Report',
            report_type='partner_summary',
            data=data,
            generated_by=request.user
        )

        if not REPORTLAB_AVAILABLE:
            return Response({'error': 'reportlab not installed on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lines = [f"Total partners: {data['total_partners']}", "", 'By type:']
        for t, cnt in data['by_type'].items():
            lines.append(f"- {t}: {cnt}")
        lines.append('')
        lines.append('By engagement level:')
        for lvl, cnt in data['by_engagement_level'].items():
            lines.append(f"- {lvl}: {cnt}")

        pdf = _create_pdf_bytes(report.title, lines)
        if pdf is None:
            return Response({'error': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resp = HttpResponse(pdf, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="report_{report.id}_partners.pdf"'
        return resp

    @action(detail=False, methods=['post'])
    def generate_engagement_analytics_pdf(self, request):
        """Generate engagement analytics report and return PDF"""
        total_engagements = Engagement.objects.count()
        by_type = dict(
            Engagement.objects.values_list('engagement_type').annotate(count=Count('id'))
        )

        top_partners_qs = Partner.objects.annotate(engagement_count=Count('engagements')).order_by('-engagement_count')[:10]
        top_partners = [{ 'name': p.name, 'count': p.engagement_count } for p in top_partners_qs]

        data = {
            'total_engagements': total_engagements,
            'by_type': by_type,
            'top_partners': top_partners,
        }

        report = Report.objects.create(
            title='Engagement Analytics Report',
            report_type='engagement_analytics',
            data=data,
            generated_by=request.user
        )

        if not REPORTLAB_AVAILABLE:
            return Response({'error': 'reportlab not installed on server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lines = [f"Total engagements: {data['total_engagements']}", '', 'By type:']
        for t, cnt in data['by_type'].items():
            lines.append(f"- {t}: {cnt}")
        lines.append('')
        lines.append('Top partners:')
        for p in data['top_partners']:
            lines.append(f"- {p['name']}: {p['count']}")

        pdf = _create_pdf_bytes(report.title, lines)
        if pdf is None:
            return Response({'error': 'PDF generation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resp = HttpResponse(pdf, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="report_{report.id}_engagements.pdf"'
        return resp
