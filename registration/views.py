from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms


# Create your views here.
def sign_up(request):
    """Multi-step volunteer registration"""
    # Get the current step from session or URL
    step = int(request.session.get('volunteer_step', 1))
    
    context = {
        'form': None,
        'errors': None,
        'user': request.user,
        'step': step,
        'total_steps': 8,
        'progress': int((step / 8) * 100)
    }
    
    # If user is already logged in, redirect to home
    if request.user.username:
        return redirect('home')
    
    # Handle form submission for each step
    if request.method == "POST":
        form_data = request.POST.copy()
        
        if step == 1:
            # Step 1: Account Information
            form = VolunteerStep1Form(form_data)
            if form.is_valid():
                # Validate passwords match
                if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                    form.add_error('password2', 'Passwords do not match')
                    context['form'] = form
                    return render(request, 'register.html', context)
                
                # Check if username exists
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    form.add_error('username', 'Username already exists')
                    context['form'] = form
                    return render(request, 'register.html', context)
                
                # Check if email exists
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    form.add_error('email', 'Email already registered')
                    context['form'] = form
                    return render(request, 'register.html', context)
                
                # Save step 1 data to session (including first_name, last_name, phone_number)
                request.session['volunteer_first_name'] = form.cleaned_data['first_name']
                request.session['volunteer_last_name'] = form.cleaned_data['last_name']
                request.session['volunteer_phone_number'] = form.cleaned_data['phone_number']
                request.session['volunteer_username'] = form.cleaned_data['username']
                request.session['volunteer_email'] = form.cleaned_data['email']
                request.session['volunteer_password'] = form.cleaned_data['password1']
                request.session['volunteer_step'] = 2
                return redirect('volunteer_register_step', step=2)
            else:
                context['form'] = form
                
        elif step == 2:
            # Step 2: Previous Connection
            form = VolunteerStep2Form(form_data)
            if form.is_valid():
                request.session['volunteer_employed_before'] = form.cleaned_data['employed_or_volunteered_before']
                request.session['volunteer_hopecare_employment_details'] = form.cleaned_data.get('hopecare_employment_details', '')
                request.session['volunteer_step'] = 3
                return redirect('volunteer_register_step', step=3)
            else:
                context['form'] = form
                
        elif step == 3:
            # Step 3: How did you hear about us
            form = VolunteerStep3Form(form_data)
            if form.is_valid():
                request.session['volunteer_how_hear'] = form.cleaned_data['how_did_you_hear']
                request.session['volunteer_how_hear_other'] = form.cleaned_data.get('volunteer_how_hear_other', '')
                request.session['volunteer_step'] = 4
                return redirect('volunteer_register_step', step=4)
            else:
                context['form'] = form
                
        elif step == 4:
            # Step 4: Motivation
            form = VolunteerStep4Form(form_data)
            if form.is_valid():
                request.session['volunteer_reasons'] = form.cleaned_data['reasons_for_volunteering']
                request.session['volunteer_step'] = 5
                return redirect('volunteer_register_step', step=5)
            else:
                context['form'] = form
                
        elif step == 5:
            # Step 5: Volunteer Interests
            form = VolunteerStep5Form(form_data)
            if form.is_valid():
                request.session['volunteer_interest'] = form.cleaned_data['volunteer_interest']
                request.session['volunteer_interest_other'] = form.cleaned_data.get('volunteer_interest_other', '')
                request.session['volunteer_step'] = 6
                return redirect('volunteer_register_step', step=6)
            else:
                context['form'] = form
                
        elif step == 6:
            # Step 6: Availability
            form = VolunteerStep6Form(form_data)
            if form.is_valid():
                request.session['volunteer_availability'] = form.cleaned_data['availability']
                request.session['volunteer_availability_details'] = form.cleaned_data.get('availability_details', '')
                request.session['volunteer_step'] = 7
                return redirect('volunteer_register_step', step=7)
            else:
                context['form'] = form
                
        elif step == 7:
            # Step 7: Employment Status
            form = VolunteerStep7Form(form_data)
            if form.is_valid():
                request.session['volunteer_employment_status'] = form.cleaned_data['employment_status']
                request.session['volunteer_employment_details'] = form.cleaned_data.get('employment_details', '')
                request.session['volunteer_step'] = 8
                return redirect('volunteer_register_step', step=8)
            else:
                context['form'] = form
                
        elif step == 8:
            # Step 8: Skills and Certification - Final Submission
            form = VolunteerStep8Form(form_data)
            if form.is_valid():
                # Get session data
                username = request.session.get('volunteer_username')
                email = request.session.get('volunteer_email')
                password = request.session.get('volunteer_password')
                first_name = request.session.get('volunteer_first_name')
                last_name = request.session.get('volunteer_last_name')
                
                # Check if username already exists (defensive check - in case session data is stale)
                if User.objects.filter(username=username).exists():
                    # Clear session and redirect to step 1 with error
                    for key in list(request.session.keys()):
                        if key.startswith('volunteer_'):
                            del request.session[key]
                    messages.error(request, 'Username already exists. Please start registration again.')
                    return redirect('sign_up')
                
                # Check if email already exists (defensive check - in case session data is stale)
                if User.objects.filter(email=email).exists():
                    # Clear session and redirect to step 1 with error
                    for key in list(request.session.keys()):
                        if key.startswith('volunteer_'):
                            del request.session[key]
                    messages.error(request, 'Email already registered. Please start registration again.')
                    return redirect('sign_up')
                
                # Create user account with first_name and last_name
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create volunteer application with phone_number
                volunteer_application = VolunteerApplication.objects.create(
                    user=user,
                    phone_number=request.session.get('volunteer_phone_number', ''),
                    employed_or_volunteered_before=request.session.get('volunteer_employed_before', 'No'),
                    hopecare_employment_details=request.session.get('volunteer_hopecare_employment_details', ''),
                    how_did_you_hear=request.session.get('volunteer_how_hear', ''),
                    how_did_you_hear_other=request.session.get('volunteer_how_hear_other', ''),
                    reasons_for_volunteering=request.session.get('volunteer_reasons', ''),
                    volunteer_interest=request.session.get('volunteer_interest', ''),
                    volunteer_interest_other=request.session.get('volunteer_interest_other', ''),
                    availability=request.session.get('volunteer_availability', ''),
                    availability_details=request.session.get('volunteer_availability_details', ''),
                    employment_status=request.session.get('volunteer_employment_status', ''),
                    employment_details=request.session.get('volunteer_employment_details', ''),
                    special_skills=form.cleaned_data['special_skills'],
                    certification=form.cleaned_data['certification'],
                    status='pending'
                )
                
                # Clear session data
                for key in list(request.session.keys()):
                    if key.startswith('volunteer_'):
                        del request.session[key]
                
                # Log the user in
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                
                messages.success(request, 'Your volunteer application has been submitted successfully!')
                return redirect('home')
            else:
                context['form'] = form
    else:
        # Initialize form based on step
        if step == 1:
            context['form'] = VolunteerStep1Form()
        elif step == 2:
            context['form'] = VolunteerStep2Form()
        elif step == 3:
            context['form'] = VolunteerStep3Form()
        elif step == 4:
            context['form'] = VolunteerStep4Form()
        elif step == 5:
            context['form'] = VolunteerStep5Form()
        elif step == 6:
            context['form'] = VolunteerStep6Form()
        elif step == 7:
            context['form'] = VolunteerStep7Form()
        elif step == 8:
            context['form'] = VolunteerStep8Form()
    
    return render(request, 'register.html', context)


def volunteer_register_step(request, step):
    """Handle individual steps of volunteer registration"""
    # Validate step parameter
    try:
        step = int(step)
        if step < 1 or step > 8:
            # Invalid step, redirect to step 1
            request.session['volunteer_step'] = 1
            return redirect('sign_up')
    except (ValueError, TypeError):
        request.session['volunteer_step'] = 1
        return redirect('sign_up')
    
    request.session['volunteer_step'] = step
    return redirect('sign_up')


def sign_in(request):
    if request.user.username:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        # Support both 'password' and 'password1' field names for backward compatibility
        password = request.POST.get('password') or request.POST.get('password1', '')
        
        if not username or not password:
            return render(request, 'login.html', {'error': 'Please enter both username and password'})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def sign_out(request):
    logout(request)
    return redirect('landing')


def home(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')
    return render(request, 'home.html', {'user': request.user})


def landing(request):
    """Public landing page - accessible to all users"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


def features(request):
    """Features page - accessible to all users"""
    return render(request, 'features.html')


def about(request):
    """About page - accessible to all users"""
    return render(request, 'about.html')


def who_we_are(request):
    """Who We Are page - accessible to all users"""
    return render(request, 'who_we_are.html')


def what_we_do(request):
    """What We Do page - accessible to all users"""
    return render(request, 'what_we_do.html')


def our_core(request):
    """Our Core page - accessible to all users"""
    return render(request, 'our_core.html')


def our_team(request):
    """Our Team page - accessible to all users"""
    from .models import TeamMember
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    return render(request, 'our_team.html', {'team_members': team_members})


def contact(request):
    """Contact page - accessible to all users"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message to the database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

