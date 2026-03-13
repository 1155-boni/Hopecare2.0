from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import VolunteerApplication, ContactMessage


class ContactForm(forms.Form):
    """Form for contact page submissions"""
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Your Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='Subject',
        widget=forms.TextInput(attrs={
            'placeholder': 'What is this about?',
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        required=True,
        label='Message',
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your message here...',
            'class': 'form-control',
            'rows': 5
        })
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Step 1: Account Information
class VolunteerStep1Form(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'})
    )
    password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )


# Step 2: Previous Connection to Hopecare
class VolunteerStep2Form(forms.Form):
    employed_or_volunteered_before = forms.ChoiceField(
        choices=[('No', 'No'), ('Yes', 'Yes')],
        widget=forms.RadioSelect,
        required=True,
        label="Have you ever been employed by, or volunteered with, Hopecare Center?"
    )
    hopecare_employment_details = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'If yes, please specify where, when, and your position or role'
        }),
        required=False,
        label="Employment/Volunteer Details"
    )


# Step 3: How did you hear about us
class VolunteerStep3Form(forms.Form):
    HEAR_CHOICES = [
        ('', 'Select an option'),
        ('website', 'Website'),
        ('social_media', 'Social Media (Facebook, Twitter, Instagram)'),
        ('friend', 'Friend or Family'),
        ('newspaper', 'Newspaper'),
        ('church', 'Church/Religious Organization'),
        ('event', 'Community Event'),
        ('newsletter', 'Newsletter/Email'),
        ('other', 'Other'),
    ]
    how_did_you_hear = forms.ChoiceField(
        choices=HEAR_CHOICES,
        required=True,
        label="How did you hear about the volunteer program at Hopecare Center?",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    how_did_you_hear_other = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'}),
        required=False,
        label="If Other, please specify"
    )


# Step 4: Motivation
class VolunteerStep4Form(forms.Form):
    reasons_for_volunteering = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Describe your main reasons for wanting to volunteer...'
        }),
        required=True,
        label="Describe your main reasons for wanting to volunteer"
    )


# Step 5: Volunteer Interests
class VolunteerStep5Form(forms.Form):
    VOLUNTEER_CHOICES = [
        ('', 'Select type of work'),
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
    volunteer_interest = forms.ChoiceField(
        choices=VOLUNTEER_CHOICES,
        required=True,
        label="Type of volunteer work that interests you",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    volunteer_interest_other = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'}),
        required=False,
        label="If Other, please specify"
    )


# Step 6: Availability
class VolunteerStep6Form(forms.Form):
    AVAILABILITY_CHOICES = [
        ('', 'Select availability'),
        ('weekdays_morning', 'Weekday Mornings'),
        ('weekdays_afternoon', 'Weekday Afternoons'),
        ('weekdays_evening', 'Weekday Evenings'),
        ('weekends_morning', 'Weekend Mornings'),
        ('weekends_afternoon', 'Weekend Afternoons'),
        ('weekends_evening', 'Weekend Evenings'),
        ('flexible', 'Flexible/As Needed'),
    ]
    availability = forms.ChoiceField(
        choices=AVAILABILITY_CHOICES,
        required=True,
        label="What is your availability?"
    )
    availability_details = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Any additional availability details...'
        }),
        required=False,
        label="Additional Availability Details"
    )


# Step 7: Employment Status
class VolunteerStep7Form(forms.Form):
    EMPLOYMENT_CHOICES = [
        ('', 'Select employment status'),
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('other', 'Other'),
    ]
    employment_status = forms.ChoiceField(
        choices=EMPLOYMENT_CHOICES,
        required=True,
        label="Are you currently employed?"
    )
    employment_details = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Please provide your employer name and job title...'
        }),
        required=False,
        label="Employment Details"
    )


# Step 8: Skills and Certification
class VolunteerStep8Form(forms.Form):
    special_skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'List any special skills, training, or qualifications you have...'
        }),
        required=True,
        label="Special skills, training or qualifications"
    )
    certification = forms.BooleanField(
        required=True,
        label="I certify that the information in this application is correct and complete to the best of my knowledge.",
        widget=forms.CheckboxInput(attrs={'class': 'certification-checkbox'})
    )

