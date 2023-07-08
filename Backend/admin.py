from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee, Department, Project, Project_Confirmation, Clock

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
#工程確認單
class Project_ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('quotation_id', 'project_name', 'order_id', 'c_a', 'client', 'requisition', 'turnover', 'is_completed', 'completion_report_employee', 'completion_report_date', 'remark', 'reassignment_attachment', 'created_date', 'update_date')
# 工作派任計畫
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('quotation_id', 'projecet_id', 'project_name', 'c_a', 'attendance_date', 'work_employee', 'lead_employee', 'vehicle', 'location', 'project_type', 'remark', 'support', 'attachment', 'created_date', 'update_date')
# 部門
class ClockAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'clock_in_or_out', 'clock_time', 'clock_GPS')


# 取消掉默認的 User model，加入擴充的 Employee 重新註冊
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Employee)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project_Confirmation, Project_ConfirmationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Clock, ClockAdmin)