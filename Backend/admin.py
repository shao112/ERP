from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import DepartmentResource, ProjectConfirmationResource, ProjectEmployeeAssignResource, ProjectJobAssignResource

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee,Equipment,UploadedFile, Approval_TargetDepartment,ApprovalModel,ApprovalLog,Department, Project_Job_Assign, Project_Confirmation, Clock,News, Project_Employee_Assign,Vehicle,Client,Requisition

admin.site.site_header = "艾力克電機後台管理"
admin.site.site_title = "艾力克電機後台"

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'

class MyUserAdmin(UserAdmin):
    inlines = (EmployeeInline, )


# 部門
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('pk','belong_to_company', 'parent_department', 'department_name', 'department_id', 'created_date', 'update_date')
    resource_class = DepartmentResource
    
# 工程確認單
class ProjectConfirmationAdmin(ImportExportModelAdmin):
    list_display = ('quotation_id',  'project_name', 'order_id', 'c_a', 'client', 'requisition', 'turnover', 'is_completed', 'display_completion_report_employee', 'completion_report_date', 'remark', 'attachment', 'created_date', 'update_date')
    def display_completion_report_employee(self, obj):
        return ', '.join([str(item) for item in obj.completion_report_employee.all()])
    display_completion_report_employee.short_description = '多對多_完工回報人'
    resource_class = ProjectConfirmationResource
    
# 工作派任計畫
class ProjectJobAssignAdmin(ImportExportModelAdmin):
    # list_display = ('project_confirmation', 'projecet_id', 'project_name', 'c_a', 'attendance_date', 'display_work_employee', 'display_lead_employee','vehicle', 'location', 'project_type', 'remark', 'support', 'attachment', 'created_date', 'update_date')
    list_display = ('project_confirmation',   'display_work_employee', 'display_lead_employee','attendance_date','vehicle', 'location', 'project_type', 'remark', 'attachment', 'created_date', 'update_date')
    # ManyToMany不能在list_display顯示
    def display_work_employee(self, obj):
        return ', '.join([str(item) for item in obj.work_employee.all()])
    display_work_employee.short_description = '多對多_工作人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班人員'
    resource_class = ProjectJobAssignResource


# 打卡
class ClockAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'clock_in_or_out', 'clock_time', 'clock_GPS',"created_date")
# 公告
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified_by')

    # list_display = [field.name for field in News._meta.get_fields()]

# 車輛
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_id', 'vehicle_type', 'created_date', 'update_date')
# 客戶
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_date', 'update_date')
# 請購單位
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ('requisition_name', 'created_date', 'update_date')
#派工單
class ProjectEmployeeAssignAdmin(ImportExportModelAdmin):
    list_display = ('project_job_assign','construction_location', 'modified_by')
    def display_inspector(self, obj):
        return ', '.join([str(item) for item in obj.inspector.all()])
    display_inspector.short_description = '多對多_檢測人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班主管'
    resource_class = ProjectEmployeeAssignResource

    # list_display = [field.name for field in Project_Employee_Assign._meta.get_fields()]

admin.site.register(Project_Employee_Assign, ProjectEmployeeAssignAdmin)

# 取消掉默認的 User model，加入擴充的 Employee 重新註冊
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Approval_TargetDepartment)
admin.site.register(ApprovalModel)
admin.site.register(ApprovalLog)
admin.site.register(News)
admin.site.register(Equipment)
admin.site.register(UploadedFile)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Employee)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project_Confirmation, ProjectConfirmationAdmin)
# admin.site.register(Data_Management, admin.ModelAdmin)
admin.site.register(Project_Job_Assign, ProjectJobAssignAdmin)
admin.site.register(Clock, ClockAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Requisition, RequisitionAdmin)