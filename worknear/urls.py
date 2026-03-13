from django.urls import path
from core import views

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
]