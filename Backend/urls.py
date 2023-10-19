from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
#打卡  
    path('check', views.Check.as_view(), name="check"),
#處理檔案
    path('delete_uploaded_file/<str:model>/<int:obj_id>/<int:file_id>', views.DeleteUploadedFileView.as_view(), name='delete_uploaded_file'),
    path('<str:model>/file', views.FileUploadView.as_view(), name='file_upload'),
    path('saveimg', views.IMGUploadView.as_view(), name='saveimg'),
    path('formuploadfile', views.FormUploadFileView.as_view(), name='formuploadfile'),
    path('excel_export', views.ExcelExportView.as_view(), name='excel_export'),

#CRUD
    path('project_confirmation',  views.Project_Confirmation_View.as_view(), name="project_confirmation_api"),
    path('equipment',  views.Equipment_View.as_view(), name="equipment_api"),
    path('department',  views.Department_View.as_view(), name="department_api"),
    path('job_assign', views.Job_Assign_View.as_view(), name="job_assign_api"),

    path('employee', views.Employee_View.as_view(), name="project_employee_api"),
    path('employee_password', views.Employee_Pasword_View.as_view(), name="employee_password"),

    path('employee_attendance', views.Employee_Attendance_View.as_view(), name="employee_attendance_api"),
    path('group', views.Groups_View.as_view(), name="groups_view_api"),
    path('approval_group', views.Approval_Groups_View.as_view(), name="approval_group_view_api"),
    path('leave_param', views.Leave_Param_View.as_view(), name="leave_param_view_api"),
    path('leave_application', views.Leave_Application_View.as_view(), name="leave_application_api"),
    path('clock_correction_application', views.Clock_Correction_Application_View.as_view(), name="clock_correction_application_api"),
    path('work_overtime_application', views.Work_Overtime_Application_View.as_view(), name="work_overtime_application_api"),
    path('project_employee_assign', views.Project_Employee_Assign_View.as_view(), name='project_employee_assign_api'),
    path('Travel_Application', views.Travel_Application_View.as_view(), name='Travel_Application_api'),
    path('profile', views.Profile_View.as_view(), name="profile_view_api"),
    path('news', views.New_View.as_view(), name="news_view_api"),
    path('calendar', views.Calendar_View.as_view(), name="calendar_api"),
    path('vehicle', views.Vehicle_View.as_view(), name="vehicle_api"),
    #處理approval 的簽核進度
    path('approval_process_log', views.Approval_Process_Log.as_view(), name="approval_process_Log_api"),
    #處理工確、派工單等的頁面處理
    path('approval_view_process', views.Approval_View_Process.as_view(), name="approval_view_process_api"),
    path('sysmessage', views.SysMessage_API.as_view(), name="approval_view_process_api"),
    path('quotation', views.Quotation_View.as_view(), name="quotation_api"),
    path('work_item', views.Work_Item_View.as_view(), name="work_item_api"),
    path('client', views.Client_View.as_view(), name="client_api"),
    path('ExtraWorkDay', views.ExtraWorkDay_View.as_view(), name="ExtraWorkDay_api"),

    # 級距表
    path('reference_table', views.ReferenceTable_View.as_view(), name="reference_table_api"),
    #計算當月所有薪資明細
    path('salary/<int:year>/<int:month>', views.SalaryListView.as_view(), name="salary_api"),
    #處理個人明細重製
    path('salary/<int:year>/<int:month>/<int:user_id>/reset', views.SalaryListView.as_view(), name="salary_only_one_api"),
    #處理明細單頁的API處理
    path('salary/<int:year>/<int:month>/<int:user>', views.SalaryDetailView.as_view(), name='salary_detail'),
    #建立薪水檔案的api
    path('salaryfile/<int:year>/<int:month>/<int:user>/<int:use_type>', views.SalaryFileView.as_view(), name='salary_file'),
    # 報價單匯出excel api
    path('quotationfile/<int:id>/<int:see>/<int:five>', views.QuotationFileView.as_view(), name='quotation_file'),

]
