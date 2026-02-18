# Alumni Partner Database

A comprehensive Django REST API system for managing alumni-partner relationships, tracking engagements, and generating analytics.

## 🚀 Quick Start

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create sample data (optional)
python create_sample_data.py

# Start server
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## 📱 Web Interfaces (All Functionalities)

### 1. **Landing Page** - `/`
- Overview of the platform
- Feature highlights
- Network statistics
- Quick action buttons
- Call-to-action sections

### 2. **User Authentication**

#### Register - `/register/`
- Alumni registration form
- Full profile setup
- Education information (degree, field of study, graduation year)
- Professional details (company, job title, industry)
- Contact information (phone, LinkedIn, email)
- Real-time validation

#### Login - `/login/`
- Username/password authentication
- Token-based session management
- Demo credentials display
- Automatic redirect to dashboard

### 3. **Dashboard** - `/dashboard/` (Requires Login)
- Personalized welcome
- Alumni profile display
- Quick statistics (alumni count, partners, engagements)
- Quick action buttons
- API documentation link
- Account information sidebar
- Logout functionality

### 4. **Alumni Directory** - `/alumni/`
- **Features:**
  - Browse all alumni profiles
  - Advanced search (name, company, industry)
  - Filtering by:
    - Degree (BA, BS, MA, MS, MBA, PhD)
    - Status (active/inactive)
    - Graduation year
    - Industry
  - Alumni cards with:
    - Profile information
    - Current employment
    - Education details
    - Contact buttons
    - LinkedIn links
  - Pagination support

### 5. **Partners Directory** - `/partners/`
- **Features:**
  - Browse all partner organizations
  - Search by organization name
  - View partner details:
    - Location
    - Website
    - Contact email
    - Description
    - Engagement level badges
  - Direct contact links
  - Pagination support

### 6. **Engagements** - `/engagements/`
- **Features:**
  - View all alumni-partner interactions
  - Filter by engagement type:
    - Mentorship
    - Recruitment
    - Speaking Event
    - Collaboration
    - Internship
  - Record new engagement modal with:
    - Alumni selection
    - Partner selection
    - Engagement type
    - Date picker
    - Outcome tracking
    - Detailed notes
  - Timeline view of all engagements
  - Search and pagination

### 7. **Analytics Dashboard** - `/analytics/`
- **Features:**
  - Key Metrics:
    - Total alumni count
    - Partner organizations count
    - Total engagements
    - Engagement rate per alumni
  - Charts & Visualizations:
    - Engagement types breakdown (doughnut chart)
    - Top engagement partners
    - Alumni by status
    - Alumni by degree
    - Industries represented
  - Report Generation:
    - Alumni summary report
    - Partner summary report
    - Engagement report

---

## 🔌 API Endpoints (All Available via Web UI)

### Alumni Endpoints
```
GET    /api/alumni/                          # List all alumni
POST   /api/alumni/                          # Create alumni
GET    /api/alumni/{id}/                     # Alumni details
PUT    /api/alumni/{id}/                     # Update alumni
DELETE /api/alumni/{id}/                     # Delete alumni
GET    /api/alumni/?search=john              # Search alumni
GET    /api/alumni/?degree=MBA               # Filter by degree
GET    /api/alumni/?status=active            # Filter by status
GET    /api/alumni/{id}/statistics/          # Alumni statistics
GET    /api/alumni/search_by_company/        # Company search
```

### Partner Endpoints
```
GET    /api/partners/                        # List all partners
POST   /api/partners/                        # Create partner
GET    /api/partners/{id}/                   # Partner details
PUT    /api/partners/{id}/                   # Update partner
DELETE /api/partners/{id}/                   # Delete partner
GET    /api/partners/top_engaged/            # Top partners by engagement
```

### Engagement Endpoints
```
GET    /api/engagements/                     # List all engagements
POST   /api/engagements/                     # Create engagement
GET    /api/engagements/{id}/                # Engagement details
PUT    /api/engagements/{id}/                # Update engagement
DELETE /api/engagements/{id}/                # Delete engagement
GET    /api/engagements/?engagement_type=mentorship  # Filter by type
```

### Analytics Endpoints
```
GET    /api/reports/                         # List all reports
POST   /api/reports/                         # Generate report
GET    /api/reports/{id}/                    # Report details
```

### Authentication Endpoints
```
POST   /auth/register/                       # Alumni registration
POST   /auth/login/                          # User login
POST   /auth/logout/                         # User logout
GET    /auth/user/                           # Current user info
GET    /api/my-profile/                      # Alumni profile management
```

---

## 🔐 Authentication

### Token-Based Authentication
1. Register at `/register/` or use API endpoint
2. Login at `/login/` or use API endpoint
3. Receive authentication token
4. Use token for API requests:
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/alumni/
   ```

### Demo Credentials
- **Username:** admin
- **Password:** admin

---

## 📊 Data Models

### Alumni
- First/Last name
- Email
- Degree (BA, BS, MA, MS, MBA, PhD)
- Field of study
- Graduation year
- Current company
- Job title
- Industry
- Phone
- LinkedIn URL
- Bio/Notes
- Status (active/inactive)
- User relationship (for authentication)

### Partner
- Organization name
- Type (corporate, non-profit, government, educational)
- Location
- Website
- Contact email
- Description
- Engagement level (low, medium, high)
- Contact person details

### Engagement
- Alumni reference
- Partner reference
- Type (mentorship, recruitment, speaking, collaboration, internship)
- Engagement date
- Outcome
- Detailed notes
- Created/updated timestamps

### Report
- Report type
- Generated data (JSON)
- Timestamp

---

## 🛠️ Technology Stack

- **Backend:** Django 4.2.10
- **API:** Django REST Framework 3.14.0
- **Authentication:** Token-based (rest_framework.authtoken)
- **Database:** PostgreSQL (production-ready), SQLite (development)
- **Documentation:** drf-spectacular (OpenAPI/Swagger)
- **Search:** django-filter
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Server:** Gunicorn (production)

---

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **ReDoc:** http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/

### Example API Calls

**Register Alumni:**
```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secure123",
    "first_name": "John",
    "last_name": "Doe",
    "degree": "MBA",
    "field_of_study": "Computer Science",
    "graduation_year": 2020,
    "current_company": "Google",
    "job_title": "Software Engineer",
    "industry": "Technology"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "username": "johndoe",
    "password": "secure123"
  }'
```

**Record Engagement:**
```bash
curl -X POST http://127.0.0.1:8000/api/engagements/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "alumni": 1,
    "partner": 1,
    "engagement_type": "mentorship",
    "engagement_date": "2026-02-17",
    "outcome": "Great mentoring session",
    "notes": "Discussed career development"
  }'
```

---

## 🌐 Navigation

### Main Menu
- **Home** - Landing page
- **Alumni** - Browse alumni directory
- **Partners** - View partner organizations
- **Engagements** - Track alumni-partner interactions
- **Analytics** - View reports and insights
- **API** - API documentation
- **Dashboard** - User dashboard (when logged in)
- **Login** - User authentication

---

## 🔒 Production Deployment

### Environment Setup
Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Deployment Steps
```bash
# Install production server
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📝 Admin Panel

Access Django admin at: `/admin/`
- Manage alumni, partners, engagements
- View user accounts
- Access logs and audit trail
- Bulk operations

---

## ✨ Features Summary

- ✅ Full-featured web UI for all operations
- ✅ RESTful API with complete documentation
- ✅ Advanced search and filtering
- ✅ Analytics and reporting
- ✅ Token-based authentication
- ✅ Responsive design (Bootstrap 5)
- ✅ Real-time data updates
- ✅ CSRF protection
- ✅ CORS support
- ✅ Pagination support
- ✅ Production-ready configuration

---

## 🐛 Troubleshooting

### CSRF Token Issues
- Ensure `X-CSRFToken` header is included in POST requests
- Token available in cookies or via form

### Authentication Errors
- Verify token is stored in localStorage
- Check token hasn't expired
- Login again if needed

### Database Issues
- Run migrations: `python manage.py migrate`
- Create sample data: `python create_sample_data.py`

---

## 📞 Support

For issues or questions:
- Check API documentation at `/api/docs/`
- Review Django admin panel at `/admin/`
- Check server logs for detailed errors

---

**Last Updated:** February 2026


A comprehensive web application for managing alumni profiles, institutional and industry partnerships, and tracking engagement between them.

## Quick Start

### Prerequisites
- Python 3.8+
- pip and virtualenv

### Installation

1. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup database**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Load sample data** (optional):
```bash
python create_sample_data.py
```

5. **Create superuser**:
```bash
python manage.py createsuperuser
```

6. **Run the server**:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

---

## Core Features & How They Work

### 0. 🔐 Alumni Registration, Login & Profile Management

**Purpose**: Allow alumni to securely register, login, and manage their own profiles.

**Key Features**:
- **Self Registration**: Alumni can register with email and password
- **Token Authentication**: Secure API access with authentication tokens
- **Profile Management**: Alumni can view and edit their own profile
- **Logout**: Revoke authentication tokens when logging out
- **Password Security**: Passwords are hashed and validated

**How to Use**:

**Register as Alumni**:
```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "degree": "BS",
    "field_of_study": "Computer Science",
    "graduation_year": 2020,
    "current_company": "Tech Corp",
    "job_title": "Software Engineer",
    "industry": "Technology"
  }'
```

**Login**:
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123"
  }'

# Response includes authentication token:
# {
#   "token": "abcd1234efgh5678ijkl9012mnop3456",
#   "user": { ... },
#   "alumni": { ... }
# }
```

**View Current Profile**:
```bash
curl -H "Authorization: Token abcd1234efgh5678ijkl9012mnop3456" \
  http://127.0.0.1:8000/auth/user/
```

**Update Profile**:
```bash
curl -X PATCH http://127.0.0.1:8000/my-profile/ \
  -H "Authorization: Token abcd1234efgh5678ijkl9012mnop3456" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Engineer",
    "current_company": "New Tech Corp",
    "bio": "Passionate about AI and machine learning"
  }'
```

**Logout**:
```bash
curl -X POST http://127.0.0.1:8000/auth/logout/ \
  -H "Authorization: Token abcd1234efgh5678ijkl9012mnop3456"
```

**Via Web Form**:
Soon! A dedicated registration and login page will be available at `/register/` and `/login/`

---

### 1. 🎓 Alumni Management

**Purpose**: Track detailed information about alumni including education, career progression, and engagement status.

**Key Features**:
- **Personal Information**: Name, email, phone number
- **Educational Background**: Degree type, field of study, graduation year
- **Professional Information**: Current company, job title, industry
- **Engagement Status**: Active, Inactive, or Lost Contact
- **Contact Methods**: LinkedIn URL, biographical information
- **Relationship Tracking**: Last engagement date

**How to Use**:

**Via API**:
```bash
# Get all alumni
curl http://127.0.0.1:8000/api/alumni/

# Get specific alumni
curl http://127.0.0.1:8000/api/alumni/1/

# Create new alumni
curl -X POST http://127.0.0.1:8000/api/alumni/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "degree": "BS",
    "field_of_study": "Computer Science",
    "graduation_year": 2020
  }'

# Filter by status
curl http://127.0.0.1:8000/api/alumni/?status=active

# Search alumni
curl http://127.0.0.1:8000/api/alumni/?search=john

# Search by company
curl http://127.0.0.1:8000/api/alumni/search_by_company/?company=Google
```

**Via Admin Panel**:
1. Go to `http://127.0.0.1:8000/admin/`
2. Navigate to "Alumni"
3. Click "Add Alumni" button
4. Fill in the form with alumni details
5. Save

**Example Workflows**:
- **Track Graduation**: Add alumni with graduation_year = 2025
- **Monitor Career Growth**: Update job_title and current_company as they progress
- **Engagement Follow-up**: Use last_engagement field to track contact frequency

---

### 2. 🏢 Partner Management

**Purpose**: Manage organizational partnerships (corporate, non-profit, government, educational institutions).

**Key Features**:
- **Organization Profile**: Name, type, description
- **Contact Information**: Email, phone, address (city, state, country)
- **Primary Contact**: Dedicated contact person details
- **Engagement Level**: Tiered partnership levels (Gold, Silver, Bronze, Prospective)
- **Business Details**: Industry, employee count, partnership start date
- **Notes & Tracking**: Internal notes and last engagement date

**How to Use**:

**Via API**:
```bash
# Get all partners
curl http://127.0.0.1:8000/api/partners/

# Get partner details
curl http://127.0.0.1:8000/api/partners/1/

# Create new partner
curl -X POST http://127.0.0.1:8000/api/partners/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Corp",
    "partner_type": "corporate",
    "email": "hr@techcorp.com",
    "engagement_level": "gold",
    "primary_contact_name": "Jane Smith",
    "primary_contact_email": "jane@techcorp.com"
  }'

# Filter by engagement level
curl http://127.0.0.1:8000/api/partners/?engagement_level=gold

# Get top engaged partners
curl http://127.0.0.1:8000/api/partners/top_engaged/?limit=10

# Search partners
curl http://127.0.0.1:8000/api/partners/?search=microsoft
```

**Via Admin Panel**:
1. Go to `http://127.0.0.1:8000/admin/`
2. Navigate to "Partners"
3. Click "Add Partner"
4. Fill organization details
5. Save

**Example Workflows**:
- **New Partnership**: Create with engagement_level = "prospective"
- **Upgrade Status**: Change from "bronze" to "silver" as engagement increases
- **Contact Management**: Store primary contact for HR/recruitment coordination

---

### 3. 🤝 Engagement Tracking

**Purpose**: Record and monitor all interactions and relationships between alumni and partners.

**Key Features**:
- **Multiple Engagement Types**: Networking events, mentorship, interviews, collaborations, donations
- **Date & Time Tracking**: When the engagement occurred
- **Description & Notes**: Details about the interaction
- **Relationship History**: Complete audit trail of alumni-partner interactions
- **Bi-directional Tracking**: Record from both alumni and partner perspective

**How to Use**:

**Via API**:
```bash
# Get all engagements
curl http://127.0.0.1:8000/api/engagements/

# Create engagement (alumni-partner interaction)
curl -X POST http://127.0.0.1:8000/api/engagements/ \
  -H "Content-Type: application/json" \
  -d '{
    "alumni": 1,
    "partner": 2,
    "engagement_type": "interview",
    "engagement_date": "2026-02-17T14:00:00Z",
    "description": "Interview for Senior Engineer position",
    "notes": "Strong candidate, good fit for team"
  }'

# Filter by engagement type
curl http://127.0.0.1:8000/api/engagements/by_type/?type=mentorship

# Get recent engagements
curl http://127.0.0.1:8000/api/engagements/recent/?limit=20

# Record engagement from alumni profile
curl -X POST http://127.0.0.1:8000/api/alumni/1/record_engagement/ \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": 2,
    "engagement_type": "networking_event",
    "engagement_date": "2026-02-17T18:00:00Z",
    "description": "Attended alumni networking dinner"
  }'

# Record engagement from partner profile
curl -X POST http://127.0.0.1:8000/api/partners/1/record_engagement/ \
  -H "Content-Type: application/json" \
  -d '{
    "alumni_id": 3,
    "engagement_type": "interview",
    "engagement_date": "2026-02-17T10:00:00Z",
    "description": "Campus recruitment interview"
  }'
```

**Example Workflows**:
- **Networking Event**: Create engagement_type = "networking_event" after alumni attends company event
- **Mentorship Program**: Track ongoing mentorship with mentorship engagement type
- **Job Placement**: Record interview → offer → hire as separate engagement records
- **Donation Tracking**: Record donation type engagement when alumni gives back

---

### 4. 📊 Analytics & Reporting

**Purpose**: Generate insights and reports on alumni and partner data for decision-making.

**Key Features**:
- **Alumni Statistics**: Breakdown by degree, graduation year, industry, status
- **Partner Analytics**: Distribution by type, engagement level, industry
- **Engagement Analytics**: Interaction patterns and trends
- **Custom Reports**: JSON-based flexible reporting
- **Admin-Controlled**: Only authenticated users can generate reports

**How to Use**:

**Via API**:
```bash
# Get alumni statistics
curl http://127.0.0.1:8000/api/alumni/statistics/
# Returns: total_alumni, active_alumni, by_degree, by_graduation_year, by_industry

# Get partner statistics
curl http://127.0.0.1:8000/api/partners/statistics/
# Returns: total_partners, by_type, by_engagement_level, by_industry

# Generate alumni summary report
curl -X POST http://127.0.0.1:8000/api/reports/generate_alumni_summary/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Generate partner summary report
curl -X POST http://127.0.0.1:8000/api/reports/generate_partner_summary/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get all reports
curl http://127.0.0.1:8000/api/reports/

# Get specific report details
curl http://127.0.0.1:8000/api/reports/1/
```

**Example Analytics Use Cases**:
- **Graduation Trends**: See which years have most active alumni
- **Industry Distribution**: Identify which industries employ most alumni
- **Partner Segments**: Understand partner mix (corporate vs non-profit)
- **Engagement Patterns**: Track which types of engagement are most successful

---

### 5. 🔍 Advanced Search & Filtering

**Purpose**: Quickly find alumni and partners using multiple criteria.

**How to Use**:

**Filtering Examples**:
```bash
# Filter alumni by multiple criteria
curl "http://127.0.0.1:8000/api/alumni/?status=active&degree=BS&graduation_year=2020"

# Filter partners by type and engagement level
curl "http://127.0.0.1:8000/api/partners/?partner_type=corporate&engagement_level=gold&industry=Technology"

# Search with text
curl "http://127.0.0.1:8000/api/alumni/?search=john+smith"
curl "http://127.0.0.1:8000/api/partners/?search=google"
```

**Pagination & Ordering**:
```bash
# Get page 2 with custom page size
curl "http://127.0.0.1:8000/api/alumni/?page=2&page_size=50"

# Order by graduation year (newest first)
curl "http://127.0.0.1:8000/api/alumni/?ordering=-graduation_year"

# Order by engagement date
curl "http://127.0.0.1:8000/api/partners/?ordering=-last_engagement"
```

---

### 6. 🔐 Admin Interface

**Purpose**: User-friendly management of all data with Django admin.

**How to Access**:
1. Visit `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage Alumni, Partners, Engagements, and Reports

**Admin Capabilities**:
- Create, read, update, delete all entities
- Advanced filtering and searching
- Bulk operations
- User and permission management
- Audit trails (created_at, updated_at timestamps)

**Default Credentials** (from sample data):
- Username: `admin`
- Password: `admin`

---

## API Documentation

### Authentication Endpoints

```bash
# Register
POST /auth/register/
{
  "username": "string",
  "email": "email@example.com",
  "password": "string (min 8 chars)",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "degree": "BS|BA|MA|MS|MBA|PhD|Other",
  "field_of_study": "string",
  "graduation_year": "number",
  "phone": "string (optional)",
  "current_company": "string (optional)",
  "job_title": "string (optional)",
  "industry": "string (optional)",
  "linkedin_url": "url (optional)",
  "bio": "string (optional)"
}
Returns: token, user, alumni

# Login
POST /auth/login/
{
  "username": "string",
  "password": "string"
}
Returns: token, user, alumni

# Get Current User
GET /auth/user/
Headers: Authorization: Token <token>
Returns: user, alumni

# Logout
POST /auth/logout/
Headers: Authorization: Token <token>
Returns: {message: "Logout successful"}

# View My Profile
GET /my-profile/
Headers: Authorization: Token <token>
Returns: alumni profile

# Update My Profile
PATCH /my-profile/
Headers: Authorization: Token <token>
{
  "job_title": "string",
  "bio": "string",
  ... other fields
}
```

### Interactive Documentation

Access interactive API docs at:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/` - Try-it-out interface
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/` - Alternative documentation
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/` - Raw schema

### Authentication

```bash
# Token authentication (for alumni)
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/my-profile/

# Session-based (for admin)
curl -b cookies.txt http://127.0.0.1:8000/api/alumni/
```

### Common Response Codes
- `200` - Success
- `201` - Created
- `400` - Bad request
- `401` - Unauthorized
- `404` - Not found
- `500` - Server error

---

## Database Models

### Alumni Model
```python
- first_name, last_name, email, phone
- degree (BA, BS, MA, MS, MBA, PhD, Other)
- field_of_study, graduation_year
- current_company, job_title, industry
- status (active, inactive, lost_contact)
- linkedin_url, bio
- created_at, updated_at, last_engagement
```

### Partner Model
```python
- name, partner_type (corporate, nonprofit, government, educational, other)
- description
- website, email, phone, address, city, state, country
- primary_contact_name, primary_contact_email, primary_contact_phone
- engagement_level (gold, silver, bronze, prospective)
- industry, employee_count, partnership_start_date
- notes, created_at, updated_at, last_engagement
```

### Engagement Model
```python
- alumni (ForeignKey)
- partner (ForeignKey)
- engagement_type (networking_event, mentorship, interview, collaboration, donation, other)
- description, engagement_date
- notes, created_at, updated_at
```

### Report Model
```python
- title, report_type (alumni_summary, partner_summary, engagement_analytics, retention_analysis)
- description
- data (JSON)
- generated_by (User)
- created_at, updated_at
```

---

## Sample Data

The app comes with sample data:
- **3 Alumni**: John Smith, Sarah Johnson, Michael Brown
- **3 Partners**: Google, Microsoft, McKinsey & Company
- **9 Engagements**: Various interactions demonstrating the system

Load with: `python create_sample_data.py`

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Clear Database and Start Fresh
```bash
rm db.sqlite3
python manage.py migrate
python create_sample_data.py
```

### Check Django Shell
```bash
python manage.py shell
>>> from core.models import Alumni
>>> Alumni.objects.all()
```

---

## Production Deployment

### Configure Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        ...
    }
}
```

### Run with Gunicorn
```bash
gunicorn config.wsgi
```

---

## Technology Stack

- **Backend**: Django 4.2.10, Django REST Framework 3.14.0
- **Database**: SQLite (dev), PostgreSQL (production)
- **API Docs**: drf-spectacular
- **Frontend**: Bootstrap 5
- **Static Files**: WhiteNoise

---

## License & Support

MIT License - Feel free to use and modify for your needs.

For questions, refer to `APP_DOCUMENTATION.md` or access API docs at `/api/docs/`
   npm start
   ```

4. **Access the application**:
   Open a web browser and go to `http://localhost:3000` to view the application.

## Contributing
Feel free to submit issues and pull requests for improvements!