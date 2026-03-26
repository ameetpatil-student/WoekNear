from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('employer-login/', views.employer_login, name='employer_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password1/', views.forgot_password1, name='forgot_password1'),
    path('jobseeker/home/', views.jobseeker_home, name='jobseeker_home'),
    path('employer/home/', views.employer_home, name='employer_home'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password1/', views.reset_password1, name='reset_password1'),
    path('add_adds/', views.add_adds, name='add_adds'),
    path('employer_register/', views.employer_register, name='employer_register'),
    path('jobseeker_home/', views.jobseeker_home, name='jobseeker_home'),
    path('employer_dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/setup-profile/', views.register_store_profile, name='register_store_profile'),
    path('admin_home_view', views.admin_home_view, name='admin_home_view'),
    path('admin_login_view', views.admin_login_view, name='admin_login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('admin_home_view', views.admin_home_view, name='admin_home_view'),
    path('approve-store/<int:store_id>/', views.approve_store_view, name='approve_store_view'),
    path('reject-store/<int:store_id>/', views.reject_store_view, name='reject_store_view'),
    path('admin/delete-store/<int:store_id>/', views.delete_store_view, name='delete_store_view'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('add-ad/', views.add_ad_view, name='add_ad'),
    path('delete-job/<int:pk>/', views.delete_job, name='delete_job'),
    path('delete-ad/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('home/', views.jobseeker_home, name='jobseeker_home'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)