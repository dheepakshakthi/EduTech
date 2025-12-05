import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def index(request):
    """View for the login page."""
    return render(request, 'index.html')

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