# Alumni Partner Database - Web Application

A centralized web system for tracking alumni profiles, industry/institutional partners, and managing their engagement relationships with comprehensive search, analytics, and reporting capabilities.

## Features

### 1. **Alumni Management**
- Track detailed alumni profiles (education, career, contact info)
- Status tracking (active, inactive, lost contact)
- Search by name, email, company, industry
- Professional information tracking (job title, company, industry)
- LinkedIn profile integration
- Last engagement tracking

### 2. **Partner Management**
- Track corporate, non-profit, government, and educational partners
- Engagement level tiers (Gold, Silver, Bronze, Prospective)
- Primary contact management
- Partnership start dates and notes
- Industry and employee count tracking
- Multiple locations support (city, state, country)

### 3. **Engagement Tracking**
- Record interactions between alumni and partners
- Engagement types: networking events, mentorship, interviews, collaborations, donations
- Timestamped engagement records with descriptions
- Track relationship history and patterns

### 4. **Analytics & Reporting**
- Alumni statistics (by degree, graduation year, industry)
- Partner statistics (by type, engagement level, industry)
- Engagement analytics and retention analysis
- Top engaged partners and alumni insights
- JSON-based reporting for flexibility
- Admin-controlled report generation

### 5. **Admin Interface**
- Django admin with customized list views
- Advanced filtering and search capabilities
- Bulk operations support
- Audit trail with created_at/updated_at timestamps
- User-friendly organization of fields

## Technology Stack

- **Backend**: Django 4.2.10 + Django REST Framework 3.14.0
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Authentication**: Session-based + REST Framework authentication
- **Filtering**: django-filter for advanced search
- **Admin**: Enhanced Django admin interface

## Project Structure

```
alumni-partner-db/
├── config/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── core/
│   ├── models.py          # Alumni, Partner, Engagement, Report models
│   ├── views.py           # REST API ViewSets
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # Core app URLs
│   ├── admin.py           # Django admin configuration
│   └── migrations/        # Database migrations
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── create_sample_data.py  # Sample data population script
└── README.md             # This file
```

## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Load Sample Data (Optional)
```bash
python create_sample_data.py
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Alumni Endpoints
- `GET/POST /api/alumni/` - List/create alumni
- `GET/PUT/DELETE /api/alumni/{id}/` - Retrieve/update/delete alumni
- `GET /api/alumni/statistics/` - Alumni statistics and analytics
- `GET /api/alumni/search_by_company/` - Search alumni by company
- `POST /api/alumni/{id}/record_engagement/` - Record alumni engagement

### Partner Endpoints
- `GET/POST /api/partners/` - List/create partners
- `GET/PUT/DELETE /api/partners/{id}/` - Retrieve/update/delete partners
- `GET /api/partners/statistics/` - Partner statistics
- `GET /api/partners/top_engaged/` - Get top engaged partners
- `POST /api/partners/{id}/record_engagement/` - Record partner engagement

### Engagement Endpoints
- `GET/POST /api/engagements/` - List/create engagements
- `GET /api/engagements/by_type/` - Filter by engagement type
- `GET /api/engagements/recent/` - Get recent engagements

### Report Endpoints
- `GET/POST /api/reports/` - List/create reports
- `POST /api/reports/generate_alumni_summary/` - Generate alumni summary
- `POST /api/reports/generate_partner_summary/` - Generate partner summary

## Query Parameters

### Filtering
```
/api/alumni/?status=active&degree=BS&graduation_year=2020
/api/partners/?partner_type=corporate&engagement_level=gold
```

### Search
```
/api/alumni/?search=john+smith
/api/partners/?search=google
```

### Pagination
```
/api/alumni/?page=1&page_size=20
```

### Ordering
```
/api/alumni/?ordering=-graduation_year
/api/partners/?ordering=-last_engagement
```

## API Documentation

### Swagger UI
Access interactive API documentation at:
```
http://127.0.0.1:8000/api/docs/
```

### ReDoc
Alternative API documentation at:
```
http://127.0.0.1:8000/api/redoc/
```

### OpenAPI Schema
Raw schema at:
```
http://127.0.0.1:8000/api/schema/
```

## Admin Interface

Access the admin panel at:
```
http://127.0.0.1:8000/admin/
```

Credentials (default from sample data):
- Username: `admin`
- Password: `admin`

## Database Models

### Alumni
- Personal info (name, email, phone)
- Education (degree, field, graduation year)
- Career (company, job title, industry)
- Engagement tracking
- Status (active/inactive/lost contact)

### Partner
- Organization info (name, type, description)
- Contact details (email, phone, address)
- Primary contact information
- Partnership details (engagement level, start date)
- Industry and employee metrics

### Engagement
- Links alumni to partners
- Engagement type (networking, mentorship, etc.)
- Date and description
- Notes and audit trail

### Report
- Generated analytics reports
- Multiple report types
- JSON data storage
- User tracking (generated_by)

## Sample Data

The `create_sample_data.py` script creates:
- 3 sample alumni (John Smith, Sarah Johnson, Michael Brown)
- 3 sample partners (Google, Microsoft, McKinsey)
- 9 engagement records between alumni and partners
- Admin superuser account (admin/admin)

## Features Highlight

✅ **Centralized Management** - All alumni and partner data in one place  
✅ **Advanced Search** - Search by name, company, industry, and more  
✅ **Analytics** - Built-in statistics and reporting  
✅ **Engagement Tracking** - Record all alumni-partner interactions  
✅ **REST API** - Full REST API with proper authentication  
✅ **API Documentation** - Auto-generated Swagger/OpenAPI docs  
✅ **Admin Interface** - Easy-to-use Django admin  
✅ **Scalable Design** - Ready for PostgreSQL and production deployment  
✅ **Filtering & Ordering** - Flexible query capabilities  
✅ **Audit Trail** - Timestamp all changes  

## Production Deployment

### Configure Settings
Update `config/settings.py` for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alumni_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
SECRET_KEY = 'your-secure-secret-key'
```

### Use Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi
```

### Environment Variables
Create `.env` file for secrets:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/alumni_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell
```bash
python manage.py shell
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
python manage.py reset_db  # Install django-extensions first
python manage.py migrate
```

### Clear Cache
```bash
python manage.py clear_cache
```

## Future Enhancements

- Frontend React/Vue.js application
- Real-time notifications
- Email integration for engagement tracking
- Advanced ML-based alumni matching
- Bulk CSV import/export
- Custom report builder
- Integration with LinkedIn API
- Automated engagement reminders
- Multi-language support

## Contributing

Contributions are welcome! Please follow PEP 8 style guide and include tests for new features.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For support, please contact the development team or create an issue in the repository.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready
