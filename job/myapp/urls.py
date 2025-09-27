from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('jobs/', views.job_list, name='job_list'),
    path('post-job/', views.post_job, name='post_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('update-resume/', views.update_resume, name='update_resume'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('view-profile/<str:user_id>/', views.view_profile, name='view_profile'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('view_applicant/<int:application_id>/', views.view_applicant, name='view_applicant'),
    path('api/categories/', views.categories_api, name='categories_api'),
]

