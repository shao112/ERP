from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required

from Backend.forms import  ProjectConfirmationForm
from Backend.models import User, Department,Project_Job_Assign, Project_Confirmation,Employee
from django.views.generic import ListView, DeleteView

from Backend.utils import get_weekly_clock_data

from django.contrib.auth.models import AnonymousUser
# 首頁
class Index(View):

    def post(self,request):
        if request.method == "POST":
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            auto_login = request.POST.get('auto-login') == 'on'
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if auto_login:
                    # Create a long-term session for auto-login
                    session = SessionStore()
                    session['user_id'] = user.id
                    session.set_expiry(1209600)  # Two weeks
                    # print("Save")
                    # print(session)
                    session.save()
                return HttpResponseRedirect('/')

    def get(self,request):
        # 0710
        # 以下寫法: employeeid = request.user.employee
        # 這樣寫出現問題: 我們登入登出頁面都做在一起，當登出時，也會跑來此get()，而user會變成AnonymousUser，AnonymousUser裡面不存在employee，頁面壞掉
        # (Django做使用者登出時，request.user變成AnonymousUser是預設行為)
        # 目前先加上判斷是不是AnonymousUser，再觀察有沒有效

        if not isinstance(request.user, AnonymousUser):
            # 使用者不是 AnonymousUser，代表是已登入的使用者
            employeeid = request.user.employee
            print(get_weekly_clock_data(employeeid))
            clock_inout = get_weekly_clock_data(employeeid)
            context = {
                'clock_inout':clock_inout,
            }
            return render(request, 'index/index-login.html', context)
        else:
            # 使用者是 AnonymousUser，代表是匿名使用者
            return render(request, 'index/index-unlogin.html')
@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


# 工程確認單，使用 ListView 顯示資料而已，做表單送出都在 Backend 的 Views.py
class Project_Confirmation_ListView(ListView):
    model = Project_Confirmation
    template_name = 'project_confirmation/project_confirmation.html'
    context_object_name = 'project_confirmation'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] =employees = Employee.objects.values('id','user__username')
        return context
    
    # 在 ListView 傳送 form
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = ProjectConfirmationForm()
    #     return context

# 工作派任計畫
class Job_Assign_ListView(ListView):
    model = Project_Job_Assign
    template_name = 'job_assign/job_assign.html'
    context_object_name = 'job_assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        return context

# 派工單
class Employee_Assign_ListView(ListView):
    model = Project_Job_Assign
    template_name = 'employee_assign/employee_assign.html'
    

# 員工
class Employee_list(ListView):
    model = Employee
    template_name = 'employee/employee.html'
    context_object_name = 'employee'
    

# 
def equipment(request):
    pass
    


from django.contrib.auth.models import Permission
# 員工權限
class Employee_Permission_list(ListView):
    model = Employee
    template_name = 'employee_permission/employee_permission.html'
    context_object_name = 'employee'
    def get_context_data(self, **kwargs):
        permissions = Permission.objects.all()
        print(permissions)
        for permission in permissions:
            print(permission.name)
            print(permission.id)


        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context['permissions'] = Permission.objects.all()
        return context
    


class Department(ListView):
    model = Department
    template_name = 'department/department.html'
    context_object_name = 'department'

    def post(self,request):
        context = {
           
        }
        return render(request, 'department/department.html', context)
    
    # CBV 要取得物件好像要使用 ListView，ListView 就不判斷 get、post，加上 get 會影響吃不到上面寫的 model
    # def get(self,request):
    #     context = {
    #     }
    #     return render(request, 'department/department.html', context)

# 基本資料
class Profile(DeleteView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'user'
