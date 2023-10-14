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

    path('project_employee_assign_View/<int:id>/',login_required(views.Project_employee_assign_View.as_view()), name='project_employee_assign_View'),

    path('approval_process', login_required(views.Approval_Process.as_view()), name="Approval_Process"),
    path('quotation', login_required(views.Quotation_ListView.as_view()), name="quotation"),
    path('salary/<int:year>/<int:month>/<int:user>', login_required(views.SalaryDetailView.as_view()), name='salary_detail'),
    path('salary/<int:year>/<int:month>', login_required(views.SalaryListView.as_view()), name='salary_list'),

    path('apply_list', login_required(views.Apply_List.as_view()), name="Apply_List"),
    path('approval_list', login_required(views.Approval_List.as_view()), name="Approval_List"),
    path('ExtraWorkDay',login_required( views.ExtraWorkDay_ListView.as_view()), name="ExtraWorkDay"),
    path('Salary_Employees', login_required(views.Salary_Employees_ListView.as_view()), name="Salary_Employees"),
    path('approval_group', login_required(views.Approval_Group.as_view()), name="Approval_Group"),
    path('leave_application', login_required(views.Leave_Application_List.as_view()), name="Leave_Application"),
    path('work_overtime_application',login_required( views.Work_Overtime_Application_List.as_view()), name="Work_Overtime_Application"),
    path('clock_correction_application', login_required(views.Clock_Correction_Application_List.as_view()), name="Clock_Correction_Application"),
    path('leave_param', login_required(views.Leave_Param_List.as_view()), name="Leave_Param"),
    path('calendar',login_required( views.Calendar.as_view()), name="calendar"),
    path('Calendar_list',login_required( views.Calendar_list.as_view()), name="Calendar_list"),
    path('director_Index', login_required(views.Director_Index.as_view()), name="director_Index"),
    path('LaborHealthInfo', login_required(views.LaborHealthInfo_ListView.as_view()), name="LaborHealthInfo"),
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
    path('client/', login_required(views.Client_ListView.as_view()), name='client_list'),

    path('news/', login_required(views.News_ListView.as_view()), name='news'),
    path('TravelApplicationView/', login_required(views.TravelApplicationView.as_view()), name='TravelApplicationView'),
    path('accounts/logout/', views.signout, name='logout'),
    #查看
    path('clock_correction_application_watch', login_required(views.Clock_Correction_Application_Watch_List.as_view()), name="clock_correction_application_watch"),
    path('leave_application_watch', login_required(views.Leave_Application_Watch_List.as_view()), name="Leave_Application_all"),
    path('work_overtime_application_watch',login_required( views.Work_Overtime_Application_Watch_List.as_view()), name="Work_Overtime_Application_watch"),
    path('TravelApplicationView_watch/', login_required(views.TravelApplicationView_Watch.as_view()), name='TravelApplicationView_watch'),
    path('approval_list_watch', login_required(views.Approval_List_Watch.as_view()), name="approval_list_Watch"),
]


