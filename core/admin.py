from django.contrib import admin

from .models import Job, Ad

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'employer', 'location', 'deadline')
    list_filter = ('job_type', 'employer')
    search_fields = ('job_title', 'description')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'created_at')
    list_filter = ('employer',)
# Register your models here.
