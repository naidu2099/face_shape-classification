from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.view_all_users, name='view_all_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
