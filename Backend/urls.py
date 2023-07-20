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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('check', views.Check.as_view(), name="check"),
    path('project_confirmation', views.Project_Confirmation_View.as_view(), name="project_confirmation_api"),
    path('<str:model>/file', views.FileUploadView.as_view(), name='file_upload'),
    path('job_assign', views.Job_Assign_View.as_view(), name="job_assign_api"),
    path('employee_assign', views.Job_Assign_View.as_view(), name="employee_assign_api"),
    path('employee', views.Employee_View.as_view(), name="project_confirmation_api"),
    path('group', views.Groups_View.as_view(), name="groups_view_api"),
]
