from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields if needed
    pass

class FCMToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fcm_tokens")
    fcm_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.fcm_token}"
