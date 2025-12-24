import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.utils.timezone import now
from .models import User

def chatbot_page(request):
    return render(request, "chatbot.html")

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

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            email = data.get("email")
            conversation_id = data.get("conversation_id")

            if not user_message:
                return JsonResponse({
                    "success": False,
                    "message": "Message is required"
                })

            # Get user and conversation if provided (for saving history)
            user = None
            conversation = None
            if email:
                user = User.objects.filter(email=email).first()
                if user and conversation_id:
                    conversation = Conversation.objects.filter(id=conversation_id, user=user).first()

            # Save user message to database
            if conversation:
                Message.objects.create(
                    conversation=conversation,
                    role='user',
                    content=user_message
                )

            payload = {
                "model": "gemma3:4b",
                "prompt": f"Explain clearly:\n{user_message}",
                "stream": False,
                "options": {
                    "num_gpu": 1,
                    "num_predict": 200  
                }
            }

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=60
            )

            result = response.json()
            bot_response = result.get("response", "")

            # Save assistant response to database
            if conversation:
                Message.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=bot_response
                )
                # Update conversation title if it's the first message
                if conversation.title == 'New Chat' and user_message:
                    conversation.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                    conversation.save()

            return JsonResponse({
                "success": True,
                "bot_response": bot_response,
                "conversation_id": conversation.id if conversation else None
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })

from .models import Conversation, Message


@csrf_exempt
def conversations_api(request):
    """
    GET: Load all conversations for a user
    POST: Create a new conversation
    DELETE: Delete a conversation
    """
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'User not found'})

            conversations = Conversation.objects.filter(user=user, is_active=True)
            
            data = []
            for conv in conversations:
                data.append({
                    'id': conv.id,
                    'title': conv.title,
                    'created_at': conv.created_at.isoformat(),
                    'updated_at': conv.updated_at.isoformat()
                })

            return JsonResponse({'success': True, 'data': data})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            title = data.get('title', 'New Chat')

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'User not found'})

            conversation = Conversation.objects.create(user=user, title=title)

            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id,
                'message': 'Conversation created'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            conversation_id = data.get('conversation_id')

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'User not found'})

            conversation = Conversation.objects.filter(id=conversation_id, user=user).first()
            if not conversation:
                return JsonResponse({'success': False, 'message': 'Conversation not found'})

            # Soft delete
            conversation.is_active = False
            conversation.save()

            return JsonResponse({'success': True, 'message': 'Conversation deleted'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def messages_api(request):
    """
    GET: Load all messages for a conversation
    """
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            conversation_id = request.GET.get('conversation_id')

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'success': False, 'message': 'User not found'})

            conversation = Conversation.objects.filter(id=conversation_id, user=user).first()
            if not conversation:
                return JsonResponse({'success': False, 'message': 'Conversation not found'})

            messages = Message.objects.filter(conversation=conversation)

            data = []
            for msg in messages:
                data.append({
                    'id': msg.id,
                    'role': msg.role,
                    'content': msg.content,
                    'created_at': msg.created_at.isoformat()
                })

            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id,
                'title': conversation.title,
                'data': data
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Only GET allowed'})

