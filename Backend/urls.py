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
    path('leave_param', views.Leave_Param_View.as_view(), name="leave_param_view_api"),
    path('project_employee_assign', views.Project_Employee_Assign_View.as_view(), name='project_employee_assign_api'),
    path('profile', views.Profile_View.as_view(), name="profile_view_api"),
    path('news', views.New_View.as_view(), name="news_view_api"),
    path('calendar', views.Calendar_View.as_view(), name="calendar_api"),
    #處理approval 的簽核進度
    path('approval_process_log', views.Approval_Process_Log.as_view(), name="approval_process_Log_api"),
    #處理工確、派工單等的頁面處理
    path('approval_view_process', views.Approval_View_Process.as_view(), name="approval_view_process_api"),
    path('sysmessage', views.SysMessage_API.as_view(), name="approval_view_process_api"),
    path('work_item', views.Work_Item_View.as_view(), name="work_item_api"),
    path('quotation', views.Quotation_View.as_view(), name="quotation_api"),
    #計算當月所有
    path('salary/<int:employee_id>/<int:file_id>', views.SalaryListView.as_view(), name="salary_api"),
    #處理明細
    path('salary/<int:year>/<int:month>/<int:user>', views.SalaryDetailView.as_view(), name='salary_detail'),

]
