from django.contrib import admin
from .models import User, Subject, Recommendation, Session


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'started_at')
    list_filter = ('subject', 'started_at')
    search_fields = ('title', 'user__name')
