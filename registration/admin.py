from django.contrib import admin
from .models import VolunteerApplication, ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'employment_status', 'volunteer_interest', 'status', 'created_at')
    list_filter = ('status', 'employment_status', 'volunteer_interest', 'created_at')
    search_fields = ('user__username', 'user__email', 'reasons_for_volunteering', 'special_skills')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Previous Connection', {
            'fields': ('employed_or_volunteered_before', 'hopecare_employment_details')
        }),
        ('Application Details', {
            'fields': ('how_did_you_hear', 'how_did_you_hear_other', 'reasons_for_volunteering')
        }),
        ('Volunteer Interests', {
            'fields': ('volunteer_interest', 'volunteer_interest_other', 'availability', 'availability_details')
        }),
        ('Employment Information', {
            'fields': ('employment_status', 'employment_details')
        }),
        ('Skills & Qualifications', {
            'fields': ('special_skills',)
        }),
        ('Certification', {
            'fields': ('certification',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
