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
#打卡  
    path('check', views.Check.as_view(), name="check"),
#處理檔案
    path('delete_uploaded_file/<int:employee_id>/<int:file_id>', views.DeleteUploadedFileView.as_view(), name='delete_uploaded_file'),
    path('<str:model>/file', views.FileUploadView.as_view(), name='file_upload'),
    path('saveimg', views.IMGUploadView.as_view(), name='saveimg'),
    path('formuploadfile', views.FormUploadFileView.as_view(), name='formuploadfile'),
    path('excel_export', views.ExcelExportView.as_view(), name='excel_export'),
    path('project_employee_assign_update_signature', views.Employee_assign_update_signature.as_view(), name='formuploadfile'),
#CRUD
    path('project_confirmation',  views.Project_Confirmation_View.as_view(), name="project_confirmation_api"),
    path('equipment',  views.Equipment_View.as_view(), name="equipment_api"),
    path('department',  views.Department_View.as_view(), name="department_api"),
    path('job_assign', views.Job_Assign_View.as_view(), name="job_assign_api"),
    path('employee', views.Employee_View.as_view(), name="project_employee_api"),
    path('employee_attendance', views.Employee_Attendance_View.as_view(), name="employee_attendance_api"),
    path('group', views.Groups_View.as_view(), name="groups_view_api"),
    path('approval_group', views.Approval_Groups_View.as_view(), name="approval_group_view_api"),
    path('project_employee_assign', views.Project_Employee_Assign_View.as_view(), name='project_employee_assign_api'),
    path('profile', views.Profile_View.as_view(), name="profile_view_api"),
    path('news', views.New_View.as_view(), name="news_view_api"),
    path('calendar', views.Calendar_View.as_view(), name="calendar_api"),
    path('approval_process', views.Approval_Process_View.as_view(), name="approval_process_view_api"),
    path('work_item', views.Work_Item_View.as_view(), name="work_item_api"),
    path('quotation', views.Quotation_View.as_view(), name="quotation_api"),

]
