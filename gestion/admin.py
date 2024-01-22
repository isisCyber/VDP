# gestion/admin.py
from django.contrib import admin
from .models import UserProfile, NewsArticle

admin.site.register(UserProfile)
admin.site.register(NewsArticle)
