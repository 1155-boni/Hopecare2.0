from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email Address")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Read")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class VolunteerApplication(models.Model):
    """Model to store volunteer application information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_application')
    
    # Phone number
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone Number",
        help_text="Please provide a contact phone number"
    )
    
    # Employment/Volunteer history with Hopecare
    employed_or_volunteered_before = models.CharField(
        max_length=3,
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No'
    )
    hopecare_employment_details = models.TextField(
        blank=True,
        verbose_name="If yes, please specify where, when, and your position or role",
        help_text="Please provide details about your previous employment or volunteer work"
    )
    
    # How they heard about the program
    how_did_you_hear = models.CharField(
        max_length=255,
        verbose_name="How did you hear about the volunteer program at Hopecare Center?",
        help_text="e.g., Website, Social Media, Friend, Newspaper, etc."
    )
    
    # Main reasons for wanting to volunteer
    reasons_for_volunteering = models.TextField(
        verbose_name="Describe your main reasons for wanting to volunteer",
        help_text="Tell us what motivates you to volunteer with Hopecare"
    )
    
    # Type of volunteer work interested in
    VOLUNTEER_CHOICES = [
        ('teaching', 'Teaching/Tutoring'),
        ('mentoring', 'Mentoring'),
        ('caregiving', 'Child Caregiving'),
        ('admin', 'Administrative Work'),
        ('events', 'Event Planning'),
        ('fundraising', 'Fundraising'),
        ('outreach', 'Community Outreach'),
        ('technical', 'Technical/IT Support'),
        ('other', 'Other'),
    ]
    volunteer_interest = models.CharField(
        max_length=50,
        choices=VOLUNTEER_CHOICES,
        verbose_name="Type of volunteer work that interests you"
    )
    volunteer_interest_other = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="If Other, please specify"
    )
    
    # Availability
    AVAILABILITY_CHOICES = [
        ('weekdays_morning', 'Weekday Mornings'),
        ('weekdays_afternoon', 'Weekday Afternoons'),
        ('weekdays_evening', 'Weekday Evenings'),
        ('weekends_morning', 'Weekend Mornings'),
        ('weekends_afternoon', 'Weekend Afternoons'),
        ('weekends_evening', 'Weekend Evenings'),
        ('flexible', 'Flexible/As Needed'),
    ]
    availability = models.CharField(
        max_length=50,
        choices=AVAILABILITY_CHOICES,
        verbose_name="What is your availability?"
    )
    availability_details = models.TextField(
        blank=True,
        verbose_name="Additional availability details",
        help_text="Please provide any additional information about your schedule"
    )
    
    # Current employment status
    EMPLOYMENT_CHOICES = [
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('other', 'Other'),
    ]
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
        verbose_name="Are you currently employed?"
    )
    employment_details = models.TextField(
        blank=True,
        verbose_name="Employment details",
        help_text="Please provide your employer name and job title if employed"
    )
    
    # Special skills, training or qualifications
    special_skills = models.TextField(
        verbose_name="Special skills, training or qualifications you would like to use in your volunteer role",
        help_text="List any relevant skills, certifications, training, or experience"
    )
    
    # Certification statement
    certification = models.BooleanField(
        default=False,
        verbose_name="I certify that the information in this application is correct and complete to the best of my knowledge."
    )
    
    # Application status
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Volunteer Application"
        verbose_name_plural = "Volunteer Applications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Volunteer Application - {self.user.username}"


class TeamMember(models.Model):
    """Model for team members to enable admin image uploads."""
    name = models.CharField(max_length=100, verbose_name="Full Name")
    role = models.CharField(max_length=100, verbose_name="Role/Position")
    bio = models.TextField(verbose_name="Bio/Description", help_text="Short bio shown on team page")
    photo = models.ImageField(
        upload_to='team/',
        verbose_name="Photo",
        help_text="Upload team member photo (recommended: 400x400px, square crop)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.name

