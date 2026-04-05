from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser


def register(request):
    """
    User registration view.
    Creates new user account with is_active=False (requires admin approval).
    """
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must wait for admin approval
            user.save()
            messages.success(request, 'Registration successful! Your account is waiting for admin approval.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    User login view.
    Only allows login for activated users.
    """
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if user exists
            try:
                user = CustomUser.objects.get(username=username)
                if not user.is_active:
                    messages.warning(request, 'Your account is waiting for admin approval.')
                    return render(request, 'accounts/login.html', {'form': form})
            except CustomUser.DoesNotExist:
                pass

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def admin_login(request):
    """
    Admin login view.
    Fixed credentials: username=admin, password=admin
    """
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Fixed admin credentials
        if username == 'mani' and password == 'Mani12@':
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                messages.success(request, 'Admin login successful!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Admin account not found. Please create superuser first.')
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'accounts/admin_login.html')


@login_required(login_url='login')
def user_dashboard(request):
    """
    User dashboard view.
    Only accessible to logged-in users.
    """
    return render(request, 'accounts/user_dashboard.html', {'user': request.user})


def user_logout(request):
    """
    Logout view for both users and admin.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
