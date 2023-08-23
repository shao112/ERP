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
from django.contrib.auth.decorators import login_required, permission_required





urlpatterns = [
    path('', views.Index.as_view(), name="index"),

    path('project_employee_assign_View/<int:id>/', views.Project_employee_assign_View.as_view(), name='project_employee_assign_View'),

    path('approval_process', views.Approval_Process.as_view(), name="Approval_Process"),
    path('quotation', views.Quotation_ListView.as_view(), name="quotation"),
    path('approval_list', views.Approval_Watch.as_view(), name="Approval_List"),
    path('calendar', views.Calendar.as_view(), name="calendar"),
    path('director_Index', views.Director_Index.as_view(), name="director_Index"),
    path('profile/', login_required(views.Profile.as_view()), name='profile'),
    path('project-confirmation/', views.Project_Confirmation_ListView.as_view(), name='project-confirmation'),
    path('department/', login_required(views.Department_list.as_view()), name='department'),
    path('equipment/', login_required(views.Equipment_ListView.as_view()), name='equipment'), 
    path('employee/', views.Employee_list.as_view(), name='employee_list'),
    path('employee_attendance/', views.Employee_Attendance_list.as_view(), name='employee_attendance'),
    path('employee_permission/', views.Employee_Permission_list.as_view(), name='employee_permission_list'),
    path('job-assign/', login_required(views.Job_Assign_ListView.as_view()), name='project'),
    path('employee_assign/', login_required(views.Employee_Assign_ListView.as_view()), name='employee_assign'),
    path('work_item/', login_required(views.Work_Item_ListView.as_view()), name='work_item_list'),
    path('news/', login_required(views.News_ListView.as_view()), name='news'),
    path('accounts/logout/', views.signout, name='logout'),
]


