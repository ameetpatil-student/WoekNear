from django.urls import path
from core import views

from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')), # This line is critical!
]