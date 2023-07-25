from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee, Department, Project_Job_Assign, Project_Confirmation, Clock,News

# Register your models here.
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'

class MyUserAdmin(UserAdmin):
    inlines = (EmployeeInline, )


# 部門
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('parent_department', 'department_name', 'department_id', 'created_date', 'update_date')
# 工程確認單
class ProjectConfirmationAdmin(admin.ModelAdmin):
    list_display = ('quotation_id', 'project_confirmation_id', 'project_name', 'order_id', 'c_a', 'client', 'requisition', 'turnover', 'is_completed', 'display_completion_report_employee', 'completion_report_date', 'remark', 'reassignment_attachment', 'created_date', 'update_date')
    def display_completion_report_employee(self, obj):
        return ', '.join([str(item) for item in obj.completion_report_employee.all()])
    display_completion_report_employee.short_description = '多對多_完工回報人'
    
# 工作派任計畫
class ProjectJobAssignAdmin(admin.ModelAdmin):
    # list_display = ('project_confirmation', 'projecet_id', 'project_name', 'c_a', 'attendance_date', 'display_work_employee', 'display_lead_employee','vehicle', 'location', 'project_type', 'remark', 'support', 'attachment', 'created_date', 'update_date')
    list_display = ('project_confirmation',  'display_work_employee', 'display_lead_employee','vehicle', 'location', 'project_type', 'remark', 'display_support_employee', 'attachment', 'created_date', 'update_date')
    # ManyToMany不能在list_display顯示
    def display_work_employee(self, obj):
        return ', '.join([str(item) for item in obj.work_employee.all()])
    display_work_employee.short_description = '多對多_工作人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班人員'
    def display_support_employee(self, obj):
        return ', '.join([str(item) for item in obj.support_employee.all()])
    display_support_employee.short_description = '多對多_支援人員'

# 派工單
class ProjectEmployeeAssignAdmin(admin.ModelAdmin):
    list_display = ('project_confirmation', 'construction_date', 'completion_date', 'is_completed', 'construction_location', 'inspector', 'vehicle', 'manuscript_return_date', 'display_lead_employee', 'author', 'enterprise_signature', 'created_date', 'update_date')
    def display_inspector(self, obj):
        return ', '.join([str(item) for item in obj.inspector.all()])
    display_inspector.short_description = '多對多_檢測人員'
    def display_lead_employee(self, obj):
        return ', '.join([str(item) for item in obj.lead_employee.all()])
    display_lead_employee.short_description = '多對多_帶班主管'

# 打卡
class ClockAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'clock_in_or_out', 'clock_time', 'clock_GPS',"created_date")
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified_by')


# 取消掉默認的 User model，加入擴充的 Employee 重新註冊
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(News)
admin.site.register(Employee)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project_Confirmation, ProjectConfirmationAdmin)
# admin.site.register(Data_Management, admin.ModelAdmin)
admin.site.register(Project_Job_Assign, ProjectJobAssignAdmin)
admin.site.register(Clock, ClockAdmin)