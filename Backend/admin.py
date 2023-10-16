from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# from .resources import DepartmentResource, ProjectConfirmationResource, ProjectEmployeeAssignResource, ProjectJobAssignResource

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Work_Item_Number,AnnualLeave, LaborHealthInfo,ReferenceTable,ExtraWorkDay,Travel_Application,SalaryDetail,Clock_Correction_Application,Work_Overtime_Application,SysMessage, Leave_Param, Leave_Application,Quotation,Work_Item, Employee,Equipment,UploadedFile, Approval_Target,ApprovalModel,ApprovalLog,Department, Project_Job_Assign, Project_Confirmation, Clock,News, Project_Employee_Assign,Vehicle,Client

admin.site.site_header = "艾力克電機後台管理"
admin.site.site_title = "艾力克電機後台"

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'
    

class MyUserAdmin(UserAdmin):
    inlines = (EmployeeInline, )

# 工項管理
class WorkItemAdmin(admin.ModelAdmin):
    pass
    # list_display = ('item_name', 'item_id', 'unit', 'unit_price', 'created_date', 'update_date')
    # resource_class = DepartmentResource
# 請假申請
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('type_of_leave', 'start_date_of_leave', 'end_date_of_leave', 'start_hours_of_leave', 'start_mins_of_leave', 'end_hours_of_leave','end_mins_of_leave','leave_hours', 'leave_mins', 'substitute', 'leave_reason', 'backlog', 'created_date', 'update_date')
    # resource_class = DepartmentResource
# 請假參數
class LeaveParamAdmin(admin.ModelAdmin):
    list_display = ('leave_name', 'leave_type', 'leave_quantity', 'minimum_leave_number', 'minimum_leave_unit', 'unit', 'is_audit', 'is_attachment', 'deduct_percentage','control','gender', 'leave_rules', 'created_date', 'update_date')
# 加班申請
class WorkOvertimeApplicationAdmin(admin.ModelAdmin):
    list_display = ('date_of_overtime',  'start_hours_of_overtime', 'start_mins_of_overtime', 'end_hours_of_overtime','end_mins_of_overtime','overtime_hours', 'overtime_mins','carry_over', 'overtime_reason', 'created_date', 'update_date')
# 補卡申請
class ClockCorrectionApplicationAdmin(admin.ModelAdmin):
    list_display = ('date_of_clock', 'shift_of_clock', 'category_of_clock', 'type_of_clock', 'end_hours_of_clock', 'end_mins_of_clock','clock_reason', 'created_date', 'update_date')

# 部門
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('pk','belong_to_company', 'parent_department', 'department_name', 'department_id', 'created_date', 'update_date')
    # resource_class = DepartmentResource
    
# 工程確認單
class ProjectConfirmationAdmin(ImportExportModelAdmin):
    list_display = ('quotation_id', 'Approval','order_id', 'c_a',   'turnover', 'is_completed', 'display_completion_report_employee', 'completion_report_date', 'remark', 'attachment', 'created_date', 'update_date')
    def display_completion_report_employee(self, obj):
        return ', '.join([str(item) for item in obj.completion_report_employee.all()])
    display_completion_report_employee.short_description = '多對多_完工回報人'
    # resource_class = ProjectConfirmationResource
    
# 工作派任計畫
class ProjectJobAssignAdmin(ImportExportModelAdmin):
    # list_display = ('project_confirmation', 'projecet_id', 'project_name', 'c_a', 'attendance_date', 'display_work_employee', 'display_lead_employee','vehicle', 'location', 'project_type', 'remark', 'support', 'attachment', 'created_date', 'update_date')
    list_display = ('project_confirmation',   'display_work_employee', 'display_lead_employee','attendance_date', 'location',  'remark', 'created_date', 'update_date')
    # ManyToMany不能在list_display顯示
    def display_work_employee(self, obj):
        return ', '.join([str(item) for item in obj.work_employee.all()])
    display_work_employee.short_description = '多對多_檢測人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班主管'
    def display_vehicle(self, obj):
        return ', '.join([str(item) for item in obj.vehicle.all()])
    display_vehicle.short_description = '多對多_車輛'
    # resource_class = ProjectJobAssignResource


# 打卡
class ClockAdmin(admin.ModelAdmin):
    list_display = ('employee_id',"clock_date", 'clock_in_or_out', 'clock_time', 'clock_GPS',"created_date")
# 公告
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified_by')


# 車輛
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_id', 'vehicle_type', 'created_date', 'update_date')
# 客戶
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_date', 'update_date')
#派工單
class ProjectEmployeeAssignAdmin(ImportExportModelAdmin):
    list_display = ("id",'project_job_assign', 'modified_by')
    def display_inspector(self, obj):
        return ', '.join([str(item) for item in obj.inspector.all()])
    display_inspector.short_description = '多對多_檢測人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班主管'
    def display_test_items(self, obj):
        return ', '.join([str(item) for item in obj.test_items.all()])
    display_test_items.short_description = '多對多_檢測項目'
    # resource_class = ProjectEmployeeAssignResource

    # list_display = [field.name for field in Project_Employee_Assign._meta.get_fields()]

class ReferenceTableAdmin(admin.ModelAdmin):
    list_display = ("location_city_residence","location_city_business_trip","amount",'name')


admin.site.register(Project_Employee_Assign, ProjectEmployeeAssignAdmin)

# 取消掉默認的 User model，加入擴充的 Employee 重新註冊
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(AnnualLeave)
admin.site.register(SysMessage)
admin.site.register(LaborHealthInfo)
admin.site.register(Travel_Application)
admin.site.register(ReferenceTable,ReferenceTableAdmin)
admin.site.register(ExtraWorkDay)
admin.site.register(SalaryDetail)
admin.site.register(Quotation)
admin.site.register(Approval_Target)
admin.site.register(ApprovalModel)
admin.site.register(ApprovalLog)
admin.site.register(News)
admin.site.register(Equipment)
admin.site.register(UploadedFile)
admin.site.register(Work_Item_Number)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Employee)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project_Confirmation, ProjectConfirmationAdmin)
# admin.site.register(Data_Management, admin.ModelAdmin)
admin.site.register(Project_Job_Assign, ProjectJobAssignAdmin)
admin.site.register(Clock, ClockAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Work_Item, WorkItemAdmin)
admin.site.register(Leave_Application, LeaveApplicationAdmin)
admin.site.register(Leave_Param, LeaveParamAdmin)
admin.site.register(Work_Overtime_Application, WorkOvertimeApplicationAdmin)
admin.site.register(Clock_Correction_Application, ClockCorrectionApplicationAdmin)