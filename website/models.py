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
