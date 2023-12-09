"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import team_members

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('accept_invite/<int:invite_id>/', views.accept_invite, name='accept_invite'),
    path('decline_invite/<int:invite_id>/', views.decline_invite, name='decline_invite'),
    path('dashboard/send-invitation/<int:user_id>/',  views.send_invitation, name='send_invitation'),
    path('dashboard/create_team/', views.create_team_view, name='create_team'),
    path('dashboard/invites/', views.invites_view, name='invites'),
    path('dashboard/My_team/', views.My_team, name='My_team'),
    path('team/<int:team_id>/members/', views.team_members, name='team_members'),
    path('create-task/', views.create_task, name='create_task'),
]
