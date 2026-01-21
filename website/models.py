from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email'], name='idx_users_email'),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"


class Subject(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)

    class Meta:
        db_table = 'subjects'
        ordering = ['title']  # Alphabetical ordering by title

    def __str__(self):
        return self.title


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=100)

    class Meta:
        db_table = 'recommendations'

    def __str__(self):
        return self.title


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    started_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sessions'

    def __str__(self):
        return f"{self.title} - {self.user.name}"


class Conversation(models.Model):
    """Stores AI chat conversations for each user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, default='New Chat')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at'], name='idx_conv_user_updated'),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.name}"


class Message(models.Model):
    """Stores individual messages within a conversation"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at'], name='idx_msg_conv_created'),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class StudyStreak(models.Model):
    """Tracks daily study activity for each user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_streaks')
    study_date = models.DateField()
    minutes_studied = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'study_streaks'
        ordering = ['-study_date']
        unique_together = ['user', 'study_date']
        indexes = [
            models.Index(fields=['user', '-study_date'], name='idx_streak_user_date'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.study_date} ({self.minutes_studied} min)"


class FocusSession(models.Model):
    """Tracks individual study sessions to analyze focus patterns"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField()
    subject = models.CharField(max_length=100)
    focus_score = models.IntegerField(default=0, help_text="Score from 1-10")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'focus_sessions'
        ordering = ['-session_date', '-start_time']
        indexes = [
            models.Index(fields=['user', '-session_date'], name='idx_focus_user_date'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.session_date} {self.start_time} ({self.duration_minutes}min)"
