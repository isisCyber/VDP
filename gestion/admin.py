# gestion/admin.py
from django.contrib import admin
from .models import UserProfile, NewsArticle, Report

admin.site.register(UserProfile)
admin.site.register(NewsArticle)
admin.site.register(Report)

