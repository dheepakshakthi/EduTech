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


def today_mission_api(request):
    if request.method == "GET":
        # Static logic now – can be dynamic later
        mission = {
            "skill_level": "Beginner",
            "mission_text": "Watch 1 video and complete 3 practice questions",
            "daily_goal_completed": False,
            "streak_message": "You usually study at 8 PM – don’t miss today"
        }

        return JsonResponse({
            "success": True,
            "today_mission": mission
        })

from datetime import date, timedelta
from .models import StudyStreak
from django.db.models import Sum

def study_streak_api(request):
    if request.method == "GET":
        try:
            email = request.GET.get('email')
            if not email:
                return JsonResponse({"success": False, "message": "Email required"})
            
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "User not found"})
            
            # Calculate current streak
            today = date.today()
            current_streak = 0
            check_date = today - timedelta(days=1)  # Start from yesterday
            
            while True:
                streak_record = StudyStreak.objects.filter(
                    user=user, 
                    study_date=check_date,
                    minutes_studied__gt=0
                ).first()
                
                if streak_record:
                    current_streak += 1
                    check_date -= timedelta(days=1)
                else:
                    break
            
            # Calculate longest streak
            all_streaks = StudyStreak.objects.filter(
                user=user,
                minutes_studied__gt=0
            ).order_by('study_date')
            
            longest_streak = 0
            temp_streak = 0
            prev_date = None
            
            for streak in all_streaks:
                if prev_date and (streak.study_date - prev_date).days == 1:
                    temp_streak += 1
                else:
                    temp_streak = 1
                
                longest_streak = max(longest_streak, temp_streak)
                prev_date = streak.study_date
            
            # Get last 7 days of data for chart
            weekly_data = []
            for i in range(6, -1, -1):
                check_date = today - timedelta(days=i)
                streak_record = StudyStreak.objects.filter(
                    user=user,
                    study_date=check_date
                ).first()
                
                day_name = check_date.strftime('%a')
                if i == 0:
                    day_name = 'Today'
                
                weekly_data.append({
                    "day": day_name,
                    "minutes": streak_record.minutes_studied if streak_record else 0,
                    "date": check_date.isoformat()
                })
            
            # Get last active date
            last_active = StudyStreak.objects.filter(
                user=user,
                minutes_studied__gt=0
            ).order_by('-study_date').first()
            
            last_active_date = last_active.study_date.isoformat() if last_active else today.isoformat()
            
            streak_data = {
                "current_streak_days": current_streak,
                "longest_streak_days": longest_streak,
                "last_active_date": last_active_date,
                "weekly_data": weekly_data,
                "streak_message": f"You are on a {current_streak}-day learning streak. Keep going!" if current_streak > 0 else "Start your streak today!"
            }

            return JsonResponse({
                "success": True,
                "study_streak": streak_data
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })

from .models import FocusSession
from django.db.models import Avg

def focus_analysis_api(request):
    if request.method == "GET":
        try:
            email = request.GET.get('email')
            if not email:
                return JsonResponse({"success": False, "message": "Email required"})
            
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "User not found"})
            
            # Get all focus sessions for this user
            sessions = FocusSession.objects.filter(user=user)
            
            if not sessions.exists():
                return JsonResponse({
                    "success": True,
                    "focus_analysis": {
                        "preferred_study_time": "No data yet",
                        "average_session_minutes": 0,
                        "focus_score": "N/A",
                        "focus_message": "Complete some study sessions to see your focus analysis."
                    }
                })
            
            # Calculate average session duration
            avg_duration = sessions.aggregate(Avg('duration_minutes'))['duration_minutes__avg']
            avg_duration = round(avg_duration) if avg_duration else 0
            
            # Calculate average focus score
            avg_score = sessions.aggregate(Avg('focus_score'))['focus_score__avg']
            avg_score = round(avg_score, 1) if avg_score else 0
            
            # Determine focus score category
            if avg_score >= 8:
                focus_category = "High"
            elif avg_score >= 6:
                focus_category = "Medium"
            else:
                focus_category = "Low"
            
            # Find preferred study time (hour with most sessions)
            time_distribution = {}
            for session in sessions:
                hour = session.start_time.hour
                time_distribution[hour] = time_distribution.get(hour, 0) + 1
            
            if time_distribution:
                preferred_hour = max(time_distribution, key=time_distribution.get)
                
                # Convert to time period
                if 5 <= preferred_hour < 12:
                    time_period = f"Morning ({preferred_hour} AM – {preferred_hour + 2} AM)"
                elif 12 <= preferred_hour < 17:
                    time_period = f"Afternoon ({preferred_hour % 12 or 12} PM – {(preferred_hour + 2) % 12 or 12} PM)"
                else:
                    time_period = f"Evening ({preferred_hour % 12 or 12} PM – {(preferred_hour + 2) % 12 or 12} PM)"
            else:
                time_period = "No preference detected"
            
            focus_data = {
                "preferred_study_time": time_period,
                "average_session_minutes": avg_duration,
                "focus_score": focus_category,
                "focus_score_value": avg_score,
                "focus_message": f"You typically focus best around {preferred_hour % 12 or 12}:00 {'PM' if preferred_hour >= 12 else 'AM'}. Try to start your session before then today."
            }

            return JsonResponse({
                "success": True,
                "focus_analysis": focus_data
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })
