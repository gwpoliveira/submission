from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('submit/', views.submission_form, name='submission_form'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-submission-status/<int:submission_id>/', views.update_submission_status, name='update_submission_status'),
    path('submissions/', views.view_submissions, name='view_submissions'),
    path('submission-success/', views.submission_success, name='submission_success'),
    path('user-submission-detail/<int:submission_id>/', views.user_submission_detail, name='user_submission_detail'),
]

