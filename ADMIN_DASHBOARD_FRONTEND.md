# Admin Dashboard - Frontend Implementation

## Overview
Created a comprehensive frontend admin dashboard that displays all admin functionalities in an easy-to-use interface.

## Access
**URL**: `http://127.0.0.1:8000/admin-dashboard/`
**Requirements**: User must be logged in with staff or superuser privileges

## Features

### 1. Dashboard Statistics
Quick overview cards showing:
- Total Alumni count
- Total Partners count
- Total Engagements count
- Total Users count

### 2. Bulk Operations Tab
**Alumni Bulk Actions:**
- Filter by status (Active, Inactive, Lost Contact)
- Actions: Mark as Active, Mark as Inactive, Mark as Lost Contact
- Shows count of alumni affected

**Partner Bulk Actions:**
- Filter by engagement level (Gold, Silver, Bronze, Prospective)
- Actions: Upgrade to Gold, Set to Silver, Set to Bronze, Downgrade to Prospective
- Shows count of partners affected

### 3. Audit Trail Tab
- View recent activity logs (last 100 actions)
- Search functionality for filtering logs
- Displays:
  - Date/Time of action
  - Action description
  - User who performed action
  - Detailed description

### 4. User Management Tab
- List all system users
- Search by username or email
- View user details:
  - Username, Email
  - Staff status
  - Active status
  - Last login date
- Actions:
  - Activate/Deactivate users with one click
  - All actions logged in audit trail

### 5. Data Exports Tab
Three export buttons for CSV downloads:
- **Export Alumni CSV**: All alumni data
- **Export Partners CSV**: All partner data
- **Export Engagements CSV**: All engagement data

All exports are logged in the audit trail.

## Navigation
The "Admin" link appears in the navigation bar only for users with staff or superuser privileges. It features a shield icon for easy identification.

## API Endpoints Created

### User Management
- `GET /api/admin/users/` - List all users
- `POST /api/admin/users/<id>/toggle-status/` - Activate/deactivate user

### Audit Logs
- `GET /api/admin/audit-logs/` - Get recent audit logs (last 100)

### Bulk Operations
- `POST /api/admin/alumni/bulk-action/` - Apply bulk action to alumni
- `POST /api/admin/partners/bulk-action/` - Apply bulk action to partners

### Data Export
- `GET /api/admin/export/alumni/` - Export alumni as CSV
- `GET /api/admin/export/partners/` - Export partners as CSV
- `GET /api/admin/export/engagements/` - Export engagements as CSV

## Security
- All admin API endpoints require `IsAdminUser` permission
- Frontend checks user status before displaying admin link
- Page redirects non-admin users to dashboard
- All admin actions are logged in audit trail with user attribution

## Audit Trail Integration
Every action performed through the admin dashboard is automatically logged:
- Bulk status changes
- Engagement level updates
- User activations/deactivations
- Data exports

Logs include:
- Timestamp
- Action description
- Username of person who performed action
- Additional details (filters applied, count affected, etc.)

## Usage Example

1. **Login as admin user**
2. **Click "Admin" in navigation** (shield icon)
3. **View dashboard statistics** at top
4. **Perform bulk operation:**
   - Select "Bulk Operations" tab
   - Choose filter (e.g., "Active" alumni)
   - Select action (e.g., "Mark as Inactive")
   - Click "Apply Action"
   - Confirm action
   - Success message shows count updated

5. **View audit trail:**
   - Select "Audit Trail" tab
   - See recent actions logged
   - Use search to filter

6. **Manage users:**
   - Select "User Management" tab
   - Search for specific user
   - Click "Activate" or "Deactivate"
   - Confirm action

7. **Export data:**
   - Select "Data Exports" tab
   - Click desired export button
   - CSV file downloads automatically

## Visual Design
- Clean, modern interface using Bootstrap 5
- Color-coded statistic cards
- Tabbed interface for organized sections
- Font Awesome icons throughout
- Responsive design for all screen sizes
- Hover effects and smooth transitions

## Integration with Django Admin
This frontend dashboard complements the Django admin panel (`/admin/`):
- **Django Admin**: For detailed record editing, complex queries
- **Frontend Dashboard**: For quick bulk operations, oversight, exports

Both systems share the same audit trail (Report model with type='audit').
