import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.utils.timezone import now
from .models import User

def index(request):
    """View for the home/landing page."""
    return render(request, 'index.html')

def auth(request):
    """View for the authentication (login/signup) page."""
    return render(request, 'auth.html')

def dashboard(request):
    """View for the dashboard page."""
    return render(request, 'dashboard.html')

@csrf_exempt  # Disabling CSRF for this specific API task to make testing easier
def signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            name = data.get('name', 'New User') # Default name if not provided

            # 1. Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})

            # 2. Create new user with HASHED password
            new_user = User(
                name=name,
                email=email,
                password_hash=make_password(password) # Never save plain text passwords!
            )
            new_user.save()

            return JsonResponse({'success': True, 'message': 'Account created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Validation (As per Task 1 image instructions)
            if not email or not password:
                return JsonResponse({'success': False, 'message': 'Email and password required'})

            # 1. Find the user by email
            user = User.objects.filter(email=email).first()

            # 2. Check if user exists AND password matches the hash
            if user and check_password(password, user.password_hash):
                return JsonResponse({'success': True, 'message': 'Login successful!', 'user': user.name})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid email or password'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


from django.db.models import Count

from .models import User, Session
def dashboard_stats_api(request):
    if request.method == 'GET':
        try:
            total_students = User.objects.count()

            today = now().date()
            active_sessions_today = Session.objects.filter(
                started_at__date=today
            ).count()

            stats = {
                "total_students": total_students,
                "active_sessions_today": active_sessions_today
            }

            return JsonResponse({
                "success": True,
                "data": stats
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })
        

def recent_sessions_api(request):
    if request.method == 'GET':
        try:
            sessions_qs = Session.objects.select_related('user') \
                .order_by('-started_at')[:3]

            sessions = []
            for s in sessions_qs:
                sessions.append({
                    "session_id": s.id,
                    "user_name": s.user.name,
                    "email": s.user.email,
                    "title": s.title,
                    "subject": s.subject,
                    "started_at": s.started_at
                })

            return JsonResponse({
                "success": True,
                "data": sessions
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })
        

from .models import Recommendation
def recommendations_api(request):
    if request.method == 'GET':
        try:
            recommendations_qs = Recommendation.objects.all()[:3]

            recommendations = []
            for r in recommendations_qs:
                recommendations.append({
                    "id": r.id,
                    "title": r.title,
                    "icon": r.icon
                })

            return JsonResponse({
                "success": True,
                "data": recommendations
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })

