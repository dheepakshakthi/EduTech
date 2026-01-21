from django.contrib import admin
from .models import User, Subject, Recommendation, Session, StudyStreak, FocusSession


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


@admin.register(StudyStreak)
class StudyStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_date', 'minutes_studied', 'tasks_completed', 'created_at')
    list_filter = ('study_date', 'user')
    search_fields = ('user__name', 'user__email')
    ordering = ('-study_date',)


@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_date', 'start_time', 'duration_minutes', 'subject', 'focus_score')
    list_filter = ('session_date', 'subject', 'user')
    search_fields = ('user__name', 'user__email', 'subject')
    ordering = ('-session_date', '-start_time')
