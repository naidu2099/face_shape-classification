from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import CustomUser
from accounts.forms import UserRegistrationForm


def is_admin(user):
    """Check if user is superuser/admin"""
    return user.is_authenticated and user.is_superuser


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    """
    Admin dashboard view.
    Shows overview and quick stats.
    """
    total_users = CustomUser.objects.filter(is_superuser=False).count()
    active_users = CustomUser.objects.filter(is_active=True, is_superuser=False).count()
    inactive_users = CustomUser.objects.filter(is_active=False, is_superuser=False).count()

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }
    return render(request, 'adminpanel/admin_dashboard.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def view_all_users(request):
    """
    View all users in table format.
    """
    users = CustomUser.objects.filter(is_superuser=False).order_by('-created_at')
    return render(request, 'adminpanel/user_list.html', {'users': users})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def activate_user(request, user_id):
    """
    Activate a user account.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} has been activated.')
    return redirect('view_all_users')


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def deactivate_user(request, user_id):
    """
    Deactivate a user account.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} has been deactivated.')
    return redirect('view_all_users')


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def delete_user(request, user_id):
    """
    Delete a user account.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f'User {username} has been deleted.')
    return redirect('view_all_users')


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def add_user(request):
    """
    Add a new user (admin can create active users directly).
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Admin-created users are active by default
            user.save()
            messages.success(request, f'User {user.username} has been created successfully.')
            return redirect('view_all_users')
    else:
        form = UserRegistrationForm()

    return render(request, 'adminpanel/add_user.html', {'form': form})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def update_user(request, user_id):
    """
    Update user information.
    """
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()
        messages.success(request, f'User {user.username} has been updated.')
        return redirect('view_all_users')

    return render(request, 'adminpanel/update_user.html', {'user': user})
