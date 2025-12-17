from django.contrib import admin
from django.urls import path
from website import views

from website.views import (
    signup_api,
    login_api,
    dashboard_stats_api,
    recent_sessions_api,
    recommendations_api
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("api/signup/", views.signup_api, name="signup_api"),
    path("api/login/", views.login_api, name="login_api"),
    path('api/dashboard/stats/', dashboard_stats_api),
    path('api/sessions/recent/', recent_sessions_api),
    path('api/recommendations/', recommendations_api),
]