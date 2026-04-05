# Quick Start Guide

## IMPORTANT: Database Setup Required

Since we added a custom user model, you need to reset the database.

### Option 1: Automatic Reset (Recommended)

1. **Stop the Django server** (if running)
2. **Run the reset script**:
   ```bash
   python reset_db.py
   ```
3. **Create migrations**:
   ```bash
   python manage.py makemigrations
   ```
4. **Setup database**:
   ```bash
   python setup_db.py
   ```
5. **Start server**:
   ```bash
   python manage.py runserver
   ```

### Option 2: Manual Reset

1. **Stop the Django server** (Ctrl+C)
2. **Manually delete** `db.sqlite3` file
3. **Delete migration files** in `accounts/migrations/` (keep `__init__.py`)
4. **Run**:
   ```bash
   python manage.py makemigrations
   python setup_db.py
   python manage.py runserver
   ```

## Access the Application

- **User Registration**: http://127.0.0.1:8000/accounts/register/
- **User Login**: http://127.0.0.1:8000/accounts/login/
- **Admin Login**: http://127.0.0.1:8000/accounts/admin-login/

## Default Admin Credentials

- Username: `admin`
- Password: `admin`

## Test the Application

1. **Register a new user** - account will be inactive
2. **Login as admin** - use admin/admin
3. **Activate the user** - go to admin dashboard → view users → activate
4. **Login as user** - now the user can access the dashboard
5. **Upload photo** - test face analysis feature

## Project Features

✓ User registration with admin approval
✓ Separate user and admin login
✓ User dashboard with face analysis
✓ Admin dashboard with user management
✓ Activate/Deactivate users
✓ Add/Edit/Delete users
✓ Modern Bootstrap 5 UI
✓ Responsive design
✓ Login-protected output page

## Troubleshooting

**Problem**: Migration errors
**Solution**: Run `python reset_db.py` then follow the steps

**Problem**: Admin user not found
**Solution**: Run `python setup_db.py`

**Problem**: Database locked
**Solution**: Stop Django server, close all programs, then run `python reset_db.py`
