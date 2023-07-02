from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee, Department

# Register your models here.
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee'

class MyUserAdmin(UserAdmin):
    inlines = (EmployeeInline, )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('parent_department', 'department_name', 'created_date', 'update_date')

# 取消掉默認的 User model，加入擴充的 Employee 重新註冊
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Department, DepartmentAdmin)