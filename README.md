# Face Analysis Django Application

## Project Structure

```
face_django_new/
├── accounts/              # User authentication app
│   ├── migrations/
│   ├── admin.py          # User admin interface
│   ├── forms.py          # Registration and login forms
│   ├── models.py         # CustomUser model
│   ├── urls.py           # Authentication URLs
│   └── views.py          # Auth views (register, login, logout)
│
├── adminpanel/           # Admin management app
│   ├── urls.py           # Admin panel URLs
│   └── views.py          # User CRUD operations
│
├── face_app/             # Main face analysis app
│   ├── gemini_gen.py     # Face analysis logic
│   ├── urls.py           # App URLs
│   └── views.py          # Protected views (login required)
│
├── templates/
│   ├── base.html         # Base template with Bootstrap 5
│   ├── accounts/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── admin_login.html
│   │   └── user_dashboard.html
│   ├── adminpanel/
│   │   ├── admin_dashboard.html
│   │   ├── user_list.html
│   │   ├── add_user.html
│   │   └── update_user.html
│   └── face_app/
│       └── results.html
│
├── config/               # Project settings
│   ├── settings.py       # Updated with custom user model
│   └── urls.py           # Main URL configuration
│
└── setup_db.py          # Database setup script
```

## Features Implemented

### 1. Authentication System
- **User Registration**: New users register with full_name, email, username, password
- **Account Activation**: Users are inactive by default, require admin approval
- **User Login**: Only activated users can login
- **Admin Login**: Separate admin login with fixed credentials (admin/admin)
- **Logout**: Secure logout for both users and admin

### 2. Custom User Model
- Extended Django's AbstractUser
- Fields: full_name, email, username, password, is_active, created_at
- Email and username are unique
- Users inactive by default (is_active=False)

### 3. User Dashboard
- Accessible only to logged-in users
- Upload photo for face analysis
- View features and benefits
- Clean navigation with profile dropdown

### 4. Admin Dashboard
- Statistics: Total users, Active users, Pending approval
- Quick action buttons
- Full user management interface

### 5. Admin User Management
- **View All Users**: Table with user details and status
- **Activate User**: Approve pending registrations
- **Deactivate User**: Suspend user accounts
- **Add User**: Create new users (active by default)
- **Update User**: Edit user information
- **Delete User**: Remove users from system

### 6. Access Control
- Output page protected with @login_required decorator
- Admin panel protected with @user_passes_test decorator
- Automatic redirects for unauthorized access

### 7. Modern UI Design
- Bootstrap 5 framework
- Responsive design (mobile-friendly)
- Bootstrap Icons
- Gradient colors and hover effects
- Card-based layouts
- Alert messages with icons

## Setup Instructions

### Step 1: Stop Any Running Django Server
Close any terminal running `python manage.py runserver`

### Step 2: Reset Database (IMPORTANT)
Since we changed the user model, you need to reset the database:

1. **Close all programs that might be using the database**
2. **Delete the old database file**: `db.sqlite3`
3. **Delete migration files** (if needed):
   - Delete all files in `accounts/migrations/` EXCEPT `__init__.py`

### Step 3: Create Migrations
```bash
python manage.py makemigrations
```

### Step 4: Run Setup Script
```bash
python setup_db.py
```

This will:
- Apply all migrations
- Create database tables
- Create admin superuser (username: admin, password: admin)

### Step 5: Run Development Server
```bash
python manage.py runserver
```

## Access URLs

- **User Registration**: http://127.0.0.1:8000/accounts/register/
- **User Login**: http://127.0.0.1:8000/accounts/login/
- **Admin Login**: http://127.0.0.1:8000/accounts/admin-login/
- **User Dashboard**: http://127.0.0.1:8000/accounts/dashboard/
- **Admin Dashboard**: http://127.0.0.1:8000/adminpanel/dashboard/

## Default Credentials

### Admin Account
- Username: `admin`
- Password: `admin`

## User Flow

### New User Registration
1. User visits registration page
2. Fills form (full_name, email, username, password)
3. Account created with `is_active=False`
4. User sees message: "Your account is waiting for admin approval"

### User Login (After Activation)
1. User enters username and password
2. If not activated: Shows "waiting for admin approval" message
3. If activated: Redirects to User Dashboard
4. User can upload photo and get face analysis

### Admin Workflow
1. Admin logs in at admin login page
2. Views admin dashboard with statistics
3. Clicks "View All Users" to see pending registrations
4. Clicks "Activate" button to approve users
5. Can also deactivate, edit, or delete users

## Technical Details

### Django Version
- Django 5.2.8
- Python 3.11.2

### Key Settings
- `AUTH_USER_MODEL = 'accounts.CustomUser'`
- `LOGIN_URL = 'login'`
- `LOGIN_REDIRECT_URL = 'user_dashboard'`

### Security Features
- CSRF protection enabled
- Password validation (Django default validators)
- Login required decorators
- User permission checks

### Database
- SQLite3 (development)
- Can be changed to PostgreSQL/MySQL for production

## Notes

- All templates use Bootstrap 5 CDN
- Responsive design works on mobile, tablet, and desktop
- Messages framework used for user feedback
- Clean, modular code with comments
- Production-ready structure

## Troubleshooting

### Migration Errors
If you see migration conflicts:
1. Delete `db.sqlite3`
2. Delete all files in `accounts/migrations/` except `__init__.py`
3. Run `python manage.py makemigrations`
4. Run `python setup_db.py`

### Admin User Not Found
Run: `python setup_db.py` to create the admin user

### Static Files Not Loading
Run: `python manage.py collectstatic`
