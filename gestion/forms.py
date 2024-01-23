# gestion/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Report, NewsArticle
from django.db import models

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['accreditation_level', 'address', 'phone_number', 'profile_image', 'department', 'position']


class ReportForm(forms.ModelForm):
    
    class Meta:
        model = Report 
        fields = ['title', 'description', 'file', 'state']

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Entrez le titre du rapport'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Entrez la description du rapport'})


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content']