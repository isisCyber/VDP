from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accreditation_level = models.CharField(max_length=50, choices=[('level1', 'Level 1'), ('level2', 'Level 2'), ('level3', 'Level 3')])
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='report_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATE_CHOICES = [
        ('soumis', 'Soumis'),
        ('en_cours', 'En cours de traitement'),
        ('resolu', 'Résolu'),
        # Ajoutez d'autres états au besoin
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='soumis')
    file = models.FileField(upload_to='report_files/', blank=True, null=True)


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)