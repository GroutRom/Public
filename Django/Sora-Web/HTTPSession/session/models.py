from django.db import models
from uuid import uuid4
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

class User(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid4, unique=True)

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, unique=True)
    type = models.CharField(max_length=10, choices=[('mobi', 'Mobile'), ('othr', 'Other')])
    vendor_uuid = models.UUIDField(null=True, blank=True)

    class Meta : 
        unique_together = ("user","type", "vendor_uuid")

class Session(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100)
    is_new_user = models.BooleanField(default=False)
    is_new_device = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    otp_code = models.CharField(max_length=6, blank=True)

    def is_expired(self):
        """
        Vérifie si la session est expirée.
        Retourne True si la session est expirée, False sinon.
        """
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiration_time