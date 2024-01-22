# gestion/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home,tableau, profile, submit_report, report_list,logout1, report_detail, report_edit, report_delete, register

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('submit-report/', submit_report, name='submit_report'),
    path('report-list/', report_list, name='report_list'),
    path('report-detail/<int:pk>/', report_detail, name='report_detail'),
    path('report-edit/<int:pk>/', report_edit, name='report_edit'),
    path('report-delete/<int:pk>/', report_delete, name='report_delete'),
    path('register/', register, name='register'),
    path('logout/', logout1, name='logout'),
    path('tableau/', tableau, name='tableau'),
]
