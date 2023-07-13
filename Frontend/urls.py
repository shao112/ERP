"""EZ9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('profile/<int:pk>', login_required(views.Profile.as_view()), name='profile'),
    path('department/', login_required(views.Department.as_view()), name='department'),
    path('equipment/', views.equipment, name='equipment'),
    path('project-confirmation/', views.Project_Confirmation_ListView.as_view(), name='project-confirmation'),
    path('employee/', views.Employee_list.as_view(), name='employee_list'),
    path('job-assign/', login_required(views.Job_Assign_ListView.as_view()), name='project'),
    path('accounts/logout/', views.signout, name='logout'),
]
