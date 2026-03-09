# TODO - Landing Page Implementation

## Plan:
- [x] 1. Create landing.html template with hero section, features, and CTAs
- [x] 2. Add landing view in registration/views.py
- [x] 3. Update registration/urls.py - route root to landing page
- [x] 4. Update home view to redirect to /home/ for authenticated users
- [x] 5. Fix settings.py - Change LOGOUT_REDIRECT_URL to '/' (was '/login/')
- [x] 6. Fix typo in settings.py - LOGINT_URL → LOGIN_URL

## Changes:
- templates/landing.html (new file) ✓
- registration/views.py (add landing view, update home redirect) ✓
- registration/urls.py (update URL routing) ✓
- templates/home.html (add navigation link) ✓
- Hopecare/settings.py (fix redirect settings) ✓

