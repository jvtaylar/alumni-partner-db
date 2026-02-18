# Copilot Instructions for Alumni Partner DB

## Project Overview
Alumni Partner DB is a Django-based REST API for managing alumni partnerships and organizational connections. It uses Django REST Framework (DRF) for API development, PostgreSQL for production data, and includes task queue support via Celery/Redis.

## Architecture

### Core Stack
- **Framework**: Django 4.2.10 with Django REST Framework 3.14.0
- **Database**: PostgreSQL (production) with psycopg2-binary driver
- **API Documentation**: drf-spectacular for automatic OpenAPI/Swagger docs
- **Task Queue**: Celery 5.3.4 with Redis 5.0.1 backend
- **Frontend Support**: django-crispy-forms with Bootstrap 4 templates
- **Testing**: pytest with pytest-django and factory-boy for fixtures

### Project Structure
```
config/          # Django settings and URL configuration
  settings.py    # Central configuration (DB, apps, middleware, secrets)
  urls.py        # Root URL routing
  wsgi.py        # Production WSGI application
manage.py        # Django management entry point
requirements.txt # Python dependencies
```

**Note**: This is an early-stage project without separate app modules yet. New features should be implemented as Django apps within the `config/` structure or as separate app directories at the root level.

## Development Workflow

### Setup
1. Create virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: Use python-decouple for environment variables (`.env` file)

### Running & Testing
- **Start development server**: `python manage.py runserver`
- **Run tests**: `python manage.py test` (as per CI workflow)
- **Database migrations**: `python manage.py migrate`
- **Create superuser**: `python manage.py createsuperuser`

### CI/CD
- GitHub Actions runs on push/PR to `main` branch
- Tests run against Python 3.7, 3.8, 3.9
- Workflow: `pip install requirements.txt` → `python manage.py test`

## Key Patterns & Conventions

### API Design
- Use DRF serializers for data validation and transformation
- Implement ViewSets for standard CRUD operations
- Apply django-filter for querystring-based filtering
- Enable CORS via django-cors-headers for frontend integration
- API docs auto-generated at `/api/schema/` via drf-spectacular

### Configuration Management
- Use `python-decouple` to load environment variables
- Never commit secrets; store SECRET_KEY and DB credentials in `.env`
- DEBUG and ALLOWED_HOSTS configured in settings.py for environment awareness

### Static Files & Media
- WhiteNoise (6.6.0) handles static file serving in production
- Pillow (10.1.0) for image processing in models/serializers
- Serve via STATIC_URL `/static/` (configurable per environment)

### Asynchronous Tasks
- Celery integration available for async operations
- Redis backend for task queue and caching
- Configure task routes in settings.py if adding new task modules

## File-Specific Guidelines

### [config/settings.py](config/settings.py)
- Update INSTALLED_APPS when creating new Django apps
- Add custom middleware carefully (execution order matters)
- Configure DATABASES for PostgreSQL connection strings
- Set CORS_ALLOWED_ORIGINS for frontend domains

### [config/urls.py](config/urls.py)
- Import and include app-level URLs using `include()`
- API versioning pattern: `/api/v1/` prefix recommended
- Admin interface auto-available at `/admin/` when configured

### [requirements.txt](requirements.txt)
- Pin exact versions (security and reproducibility)
- Test additions: pytest, pytest-django, factory-boy, faker
- Add packages using `pip freeze` or manual entry with version

## Common Tasks

**Add a new Django app**: 
```bash
python manage.py startapp app_name
# Update config/settings.py INSTALLED_APPS
# Add URL patterns to config/urls.py
```

**Create API serializers**:
Use DRF serializers in app-level `serializers.py`; leverage ModelSerializer for standard CRUD.

**Add database migrations**:
```bash
python manage.py makemigrations app_name
python manage.py migrate
```

**Debug settings**:
Set DEBUG=True locally (via `.env`); use `python manage.py shell` for interactive testing.

## External Dependencies to Know
- **drf-spectacular**: Auto-generates Swagger/OpenAPI schema
- **django-extensions**: Enhanced management commands (e.g., `shell_plus`)
- **faker**: Generate fake data for testing
- **gunicorn**: WSGI server for production deployment
