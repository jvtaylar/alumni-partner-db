import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Alumni, Partner, Engagement
from django.contrib.auth.models import User

# Create a superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: admin / admin')

# Create sample alumni
alumni_data = [
    {
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john.smith@example.com',
        'phone': '555-0101',
        'degree': 'BS',
        'field_of_study': 'Computer Science',
        'graduation_year': 2018,
        'current_company': 'Google',
        'job_title': 'Software Engineer',
        'industry': 'Technology',
        'status': 'active',
        'linkedin_url': 'https://linkedin.com/in/johnsmith',
        'bio': 'Passionate about software development and tech innovation'
    },
    {
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'email': 'sarah.johnson@example.com',
        'phone': '555-0102',
        'degree': 'MBA',
        'field_of_study': 'Business Administration',
        'graduation_year': 2020,
        'current_company': 'McKinsey',
        'job_title': 'Management Consultant',
        'industry': 'Consulting',
        'status': 'active',
        'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
        'bio': 'Strategy and business transformation consultant'
    },
    {
        'first_name': 'Michael',
        'last_name': 'Brown',
        'email': 'michael.brown@example.com',
        'phone': '555-0103',
        'degree': 'MS',
        'field_of_study': 'Data Science',
        'graduation_year': 2019,
        'current_company': 'Amazon',
        'job_title': 'Data Scientist',
        'industry': 'Technology',
        'status': 'active',
        'bio': 'Data analytics and machine learning expert'
    },
]

alumni_objs = []
for data in alumni_data:
    alumni, created = Alumni.objects.get_or_create(
        email=data['email'],
        defaults=data
    )
    alumni_objs.append(alumni)
    if created:
        print(f'Created alumni: {alumni.first_name} {alumni.last_name}')

# Create sample partners
partner_data = [
    {
        'name': 'Google',
        'partner_type': 'corporate',
        'description': 'Global technology company',
        'website': 'https://google.com',
        'email': 'partnerships@google.com',
        'phone': '650-253-0000',
        'city': 'Mountain View',
        'state': 'CA',
        'country': 'USA',
        'primary_contact_name': 'Alice Chen',
        'primary_contact_email': 'alice.chen@google.com',
        'primary_contact_phone': '650-253-1234',
        'engagement_level': 'gold',
        'industry': 'Technology',
        'employee_count': 190000,
        'partnership_start_date': '2020-01-01',
        'notes': 'Strategic technology partner'
    },
    {
        'name': 'Microsoft',
        'partner_type': 'corporate',
        'description': 'Software and cloud solutions provider',
        'website': 'https://microsoft.com',
        'email': 'partnerships@microsoft.com',
        'phone': '425-882-8080',
        'city': 'Redmond',
        'state': 'WA',
        'country': 'USA',
        'primary_contact_name': 'Bob Williams',
        'primary_contact_email': 'bob.williams@microsoft.com',
        'engagement_level': 'gold',
        'industry': 'Technology',
        'employee_count': 220000,
        'partnership_start_date': '2019-06-15',
        'notes': 'Cloud and enterprise solutions partner'
    },
    {
        'name': 'McKinsey & Company',
        'partner_type': 'corporate',
        'description': 'Global management consulting firm',
        'website': 'https://mckinsey.com',
        'email': 'careers@mckinsey.com',
        'phone': '212-446-7000',
        'city': 'New York',
        'state': 'NY',
        'country': 'USA',
        'primary_contact_name': 'Carol Davis',
        'primary_contact_email': 'carol.davis@mckinsey.com',
        'engagement_level': 'silver',
        'industry': 'Consulting',
        'employee_count': 35000,
        'partnership_start_date': '2021-03-20',
        'notes': 'Consulting and recruiting partner'
    },
]

partner_objs = []
for data in partner_data:
    partner, created = Partner.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    partner_objs.append(partner)
    if created:
        print(f'Created partner: {partner.name}')

# Create sample engagements
if alumni_objs and partner_objs:
    engagement_types = ['networking_event', 'mentorship', 'interview', 'collaboration']
    
    for i, alumni in enumerate(alumni_objs):
        for j, partner in enumerate(partner_objs):
            if not Engagement.objects.filter(alumni=alumni, partner=partner).exists():
                engagement_date = timezone.now() - timedelta(days=i*30+j*10)
                Engagement.objects.create(
                    alumni=alumni,
                    partner=partner,
                    engagement_type=engagement_types[i % len(engagement_types)],
                    description=f'Engagement between {alumni} and {partner}',
                    engagement_date=engagement_date,
                    notes='Sample engagement data'
                )
                print(f'Created engagement: {alumni} - {partner}')

print('\nSample data created successfully!')
