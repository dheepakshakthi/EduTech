from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Page Routes (HTML Views)
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("chatbot/", views.chatbot_page, name="chatbot"),

    # Authentication APIs
    path("api/signup/", views.signup_api, name="signup_api"),
    path("api/login/", views.login_api, name="login_api"),

    # Core Dashboard APIs
    path("api/dashboard/stats/", views.dashboard_stats_api),
    path("api/sessions/recent/", views.recent_sessions_api),
    path("api/recommendations/", views.recommendations_api),

    # Chatbot & Conversation APIs
    path("api/chatbot/", views.chatbot_api),
    path("api/conversations/", views.conversations_api, name="conversations_api"),
    path("api/messages/", views.messages_api, name="messages_api"),

    # Personalized Dashboard Features
    path("dashboard/today-mission/", views.today_mission_api),
    path("dashboard/study-streak/", views.study_streak_api),
    path("dashboard/focus-analysis/", views.focus_analysis_api),
]
