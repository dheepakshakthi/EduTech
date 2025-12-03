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
