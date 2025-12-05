from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),

    path("api/signup/", views.signup_api, name="signup_api"),
    path("api/login/", views.login_api, name="login_api"),
]