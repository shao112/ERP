from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required

from Backend.forms import  ProjectJobAssignForm, ClockCorrectionApplicationForm, WorkOvertimeApplicationForm, LeaveApplicationForm, ProjectConfirmationForm, EmployeeForm, NewsForm, ApprovalModelForm, DepartmentForm
from Backend.models import ReferenceTable,Travel_Application, Clock,Clock_Correction_Application,Work_Overtime_Application,Leave_Application,Salary,SalaryDetail,Leave_Param, Leave_Param, Approval_Target, Quotation, Work_Item,ApprovalModel,User, Department, Project_Job_Assign, Project_Confirmation,Project_Employee_Assign,Employee, News, Equipment, Vehicle, Client, Requisition
from django.views.generic import ListView, DeleteView,DetailView
from django.conf import settings


from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date
from django.views.defaults import permission_denied
from Backend.utils import convent_employee,get_weekly_clock_data
from django.db.models import Q,Value,CharField
from django.db.models.functions import Concat
import json



class TravelApplicationView(ListView):
    model = Travel_Application
    template_name = 'Travel_Application/Travel_Application.html'
    context_object_name = 'Travel_Applications'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Travel_Application_list"] = Travel_Application.objects.filter(applicant=self.request.user.employee)
        return context

class Project_employee_assign_View(DetailView):
    model = Project_Employee_Assign
    template_name = 'pdf/Equipment_pdf.html'
    context_object_name = 'project_employee_assign'
    pk_url_kwarg = 'id'  # This is where the 'id' parameter is mapped



class SalaryDetailView(UserPassesTestMixin,ListView):
    model = Salary
    template_name = 'Salary/SalarySingle.html'
    context_object_name = 'salary'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        user = self.kwargs.get('user')    
        context["salary"] = Salary.objects.get(user=user, year=year, month=month)
        context["work_list"] = Clock.get_hour_for_month(self.request.user.employee,year,int(month))
        return context

    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='財務').exists()    

class SalaryListView(UserPassesTestMixin,ListView):
    model = Salary
    template_name = 'Salary/Salary.html'
    context_object_name = 'salaries'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        queryset = Salary.objects.filter(year=year, month=month)
        return queryset
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='財務').exists()    
    

# 首頁
class Director_Index(View):
    def get(self,request):
            current_employee = request.user.employee
            other_employees = current_employee.departments.employees.exclude(id=current_employee.id)
            other_employees = convent_employee(other_employees)
            for employee in other_employees:
                employee['clock_data'] = get_weekly_clock_data(employee['id'])

            # print(other_employees)
            # print(other_employees[0].get_weekly_clock_data())
            context= {"other_employees":other_employees}
            return render(request, 'index/director_Index.html',context)    

class Index(View):

    def post(self,request):
        if request.method == "POST":
            belong_to_company = request.POST.get('belong_to_company', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            auto_login = request.POST.get('auto-login') == 'on'
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # belong_to_company == user.employee.departments.belong_to_company 加在上面的 if 條件
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
        # verified用來判斷是否帳號密碼錯誤，要顯示資訊欄
        verified = False
        context = {
            'verified':verified,
        }
        return render(request, 'index/index-unlogin.html', context)
        

    def get(self,request):

        if not isinstance(request.user, AnonymousUser):

            # 使用者不是 AnonymousUser，代表是已登入的使用者
            news = News.objects.all()
            employeeid = request.user.employee
            clock_inout = get_weekly_clock_data(employeeid)
            related_projects = Project_Job_Assign.objects.filter(lead_employee__in=[employeeid])|Project_Job_Assign.objects.filter(    work_employee__in=[employeeid]        )
            related_projects = related_projects.distinct()

            grouped_projects = {}
            for project in related_projects:
                if project.attendance_date:
                    date_str = project.attendance_date
                    if date_str >= date.today():
                        if date_str in grouped_projects:
                            grouped_projects[date_str].append(project)
                        else:
                            grouped_projects[date_str] = [project]
            sorted_grouped_projects = dict(sorted(grouped_projects.items()))
            
            context = {
                'clock_inout':clock_inout,
                'news':news,
                "grouped_projects":sorted_grouped_projects,
            }
            return render(request, 'index/index-login.html', context)
        else:
            # 使用者是 AnonymousUser，代表是匿名使用者
            return render(request, 'index/index-unlogin.html')
        

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

# 工程確認單
class Project_Confirmation_ListView(UserPassesTestMixin,ListView):
    model = Project_Confirmation
    template_name = 'project_confirmation/project_confirmation.html'
    context_object_name = 'project_confirmation'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["employees_list"] = Employee.objects.values('id','user__username')
        context['client_list'] = Client.objects.all()
        context['project_confirmation_form'] = ProjectConfirmationForm()
        context['quotation_list'] = Quotation.objects.all()
        return context

    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='工程確認單').exists()    
    


# 工作派任計畫
class Job_Assign_ListView(UserPassesTestMixin,ListView):
    model = Project_Job_Assign
    template_name = 'job_assign/job_assign.html'
    context_object_name = 'job_assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['project_job_assign_form'] = ProjectJobAssignForm()


        context['vehicle'] = Vehicle.objects.all()
        return context

    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='工程派任計畫').exists()    

# 派工單
class Employee_Assign_ListView(UserPassesTestMixin,ListView):
    model = Project_Employee_Assign
    template_name = 'employee_assign/employee_assign.html'
    context_object_name = 'Project_Employee_Assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] =  Employee.objects.values('id','user__username')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        return context

    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='工程派工單').exists()    

    

# 員工
class Employee_list(UserPassesTestMixin,ListView):
    model = Employee
    template_name = 'employee/employee.html'
    context_object_name = 'employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department_list"] = Department.objects.values('id','department_name')
        context['employee_form'] = EmployeeForm()
        return context
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='管理部').exists()    


# 員工出勤
class Employee_Attendance_list(UserPassesTestMixin,ListView):
    model = Employee
    template_name = 'employee_attendance/employee_attendance.html'
    context_object_name = 'employees'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        return context
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='管理部').exists()    


# 固定資產管理
class Equipment_ListView(UserPassesTestMixin,ListView):
    model = Equipment
    template_name = 'equipment/equipment.html'
    context_object_name = 'equipment'
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='管理部').exists()    

    


from django.contrib.auth.models import Group
# 員工權限
class Employee_Permission_list(UserPassesTestMixin,ListView):
    model = Employee
    template_name = 'employee_permission/employee_permission.html'
    context_object_name = 'employees'
    def get_context_data(self, **kwargs):
        groups = Group.objects.all()
        supervisor_group = groups.filter(name='主管')
        approval_group = groups.filter(name='簽核權')
        other_groups = groups.exclude(name__in=['主管', '簽核權']).order_by('name')
        
        sorted_groups = list(supervisor_group) + list(approval_group) + list(other_groups)
       
        Groups = Group.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)
        context["employees_list"] =  Employee.objects.values('user__id','user__username')
        context['groups'] = sorted_groups
        return context
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='管理部權限管理').exists()    



class Department_list(UserPassesTestMixin,ListView):
    model = Department
    template_name = 'department/department.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_form'] = DepartmentForm()
        return context

    def post(self,request):
        context = {
           
        }
        return render(request, 'department/department.html', context)
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='管理部').exists()    



# 基本資料(無法使用別人的id)
class Profile(DeleteView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    def get_object(self, queryset=None):
        # 從request.user中獲取當前用戶的id，然後返回相應的User物件
        return self.request.user

# 工項資料庫
class Work_Item_ListView(ListView):
    model = Work_Item
    template_name = 'work_item/work_item.html'
    context_object_name = 'work_item'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context





# 報價單
class Quotation_ListView(ListView):
    model = Quotation
    template_name = 'quotation/quotation.html'
    context_object_name = 'quotation'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workitems"]= Work_Item.objects.all()
        client_id = self.kwargs.get('client_id', None)
        context['client'] = Client.objects.get(id=client_id)

        if client_id:
            context['quotation'] = Quotation.objects.filter(client=client_id)
        else:
            context['quotation'] = Quotation.objects.all()

        return context

# 最新消息
class News_ListView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_form'] = NewsForm()
        return context

# 行事曆
class Calendar(ListView):
    model = Employee
    template_name = 'calendar/calendar.html'
    context_object_name = 'employee'



class Approval_List(ListView):
    model = ApprovalModel
    template_name = 'approval_list/approval_list.html'
    context_object_name = 'approval_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        current_employee = self.request.user.employee

        all_approval_models = ApprovalModel.objects.all()

        related_approval_models = [
            approval_model for approval_model in all_approval_models
            if approval_model.get_created_by == current_employee
        ]

        print(related_approval_models)



        queryset = related_approval_models
        return queryset


class Approval_Process(ListView):
    model = ApprovalModel
    template_name = 'approval_process/approval_process.html'
    context_object_name = 'approval_process'

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['vehicle'] = Vehicle.objects.all()
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["leave_application_form"] = LeaveApplicationForm()
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()

        context["24range"] = range(24)
        context["60range"] = range(60)   
        return context
    

    def get_queryset(self):
        current_employee = self.request.user.employee
    
        related_records = []
    
        for Approval in ApprovalModel.objects.filter(current_status="in_progress"):            
            get_employee = Approval.get_approval_employee()
            if get_employee !="x":
                related_records.append(Approval)
            else:
                # 取得作者部門
                get_createdby = Approval.get_created_by
                print(get_createdby)
                department =get_createdby.departments
                #撈取主管權限的員工
                supervisor_employees = department.employees.filter(user__groups__name='主管').values_list('id', flat=True)
                #判斷主管是不是在當前user
                is_supervisor = current_employee.id in supervisor_employees
                if is_supervisor:            
                   related_records.append(Approval)

        queryset=related_records
        return queryset
    

# 簽核順序
class Approval_Group(UserPassesTestMixin,ListView):
    model = Approval_Target
    template_name = 'approval_group/approval_group.html'
    context_object_name = 'approval_group'

    def test_func(self):#有簽核權
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='簽核流程管理').exists() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees"] = Employee.objects.all()
        return context


# 請假參數
class Leave_Param_List(UserPassesTestMixin,ListView):
    model = Leave_Param
    template_name = 'leave_param/leave_param.html'
    context_object_name = 'leave_param'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leave_param"] = Leave_Param.objects.all()
 
        return context
    
    def test_func(self):
        if settings.PASS_TEST_FUNC:
            return True
        return self.request.user.groups.filter(name__icontains='財務').exists()

# 請假申請
class Leave_Application_List(ListView):
    model = Leave_Application
    template_name = 'leave_application/leave_application.html'
    context_object_name = 'leave_application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leave_application_form"] = LeaveApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)

        user = self.request.user.employee

        context["leave_details"] =Leave_Param.get_leave_param_details(user)
        context["leave_application_list"] =Leave_Application.objects.filter(applicant=user)

        return context


# 加班申請
class Work_Overtime_Application_List(ListView):
    model = Work_Overtime_Application
    template_name = 'work_overtime_application/work_overtime_application.html'
    context_object_name = 'work_overtime_applicationS'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.employee
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        context["work_overtime_application_list"] =Work_Overtime_Application.objects.filter(created_by=user)
        return context
    
# 補卡申請
class Clock_Correction_Application_List(ListView):
    model = Clock_Correction_Application
    template_name = 'clock_correction_application/clock_correction_application.html'
    context_object_name = 'clock_correction_applications'

    def get_context_data(self, **kwargs):
        user = self.request.user.employee
        context = super().get_context_data(**kwargs)
        context["clock_correction_application_list"] =Clock_Correction_Application.objects.filter(created_by=user)
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        return context
    


