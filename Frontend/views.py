from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.base import  TemplateView

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from datetime import datetime

from Backend.forms import  ReferenceTableForm, VehicleForm, SalaryEmployeeForm, Travel_ApplicationForm,ProjectJobAssignForm, ClockCorrectionApplicationForm, WorkOvertimeApplicationForm, LeaveApplicationForm, ProjectConfirmationForm, EmployeeForm, NewsForm, ApprovalModelForm, DepartmentForm
from Backend.models import LaborHealthInfo  ,ExtraWorkDay,ReferenceTable,Travel_Application, Clock,Clock_Correction_Application,Work_Overtime_Application,Leave_Application,Salary,SalaryDetail,Leave_Param, Leave_Param, Approval_Target, Quotation, Work_Item,ApprovalModel,User, Department, Project_Job_Assign, Project_Confirmation,Project_Employee_Assign,Employee, News, Equipment, Vehicle, Client
from django.views.generic import ListView, DeleteView,DetailView
from django.conf import settings


from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date
from django.views.defaults import permission_denied
from Backend.utils import convent_employee,get_weekly_clock_data,Check_Permissions,convent_dict
from django.db.models import Q,Value,CharField
from django.db.models.functions import Concat
import json
from django.shortcuts import get_object_or_404
from django.http import FileResponse

class ReferenceTable_ListView(UserPassesTestMixin,ListView):
    
    model = ReferenceTable
    template_name = 'reference_table/reference_table.html'
    context_object_name = 'reference_table'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs.get('name')
        objs = ReferenceTable.objects.filter(name=name).order_by('location_city_residence')
        context['objs'] = objs
        context["name"] = name
        context['ReferenceTableForm'] = ReferenceTableForm
        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"管理部管理")


class LaborHealthInfo_ListView(UserPassesTestMixin,View):

    def post(self,request):
        dict_data = convent_dict(request.body)

        try:
            get_obj = get_object_or_404(LaborHealthInfo, id=dict_data['id'])
        except Exception as e:
            return JsonResponse({"error": "找不到相應的勞健保級距 obj"}, status=400)
        get_obj.update_fields_and_save(**dict_data)
       
        return JsonResponse({"ok":"ok"},status=200)
    
    def get(self,request):
        context ={}
        
        context["LaborHealth_list"] = LaborHealthInfo.objects.all().order_by("salary_low") 
        return render(request, 'LaborHealth/LaborHealth.html', context)

    def test_func(self):
        return Check_Permissions(self.request.user,"管理部管理")
    


# 員工薪水調整
class Salary_Employees_ListView(UserPassesTestMixin,View):

    def get(self,request):
        context ={}
        context["employees_list"] = Employee.objects.values('id','full_name')
        context["SalaryEmployeeForm"] =SalaryEmployeeForm 
     
        return render(request, 'Salary/Salary_Employees.html', context)

    def test_func(self):
        return Check_Permissions(self.request.user,"薪水管理")
    


class TravelApplicationView_Watch(UserPassesTestMixin,ListView):
    model = Travel_Application
    template_name = 'Travel_Application/Travel_Application_watch.html'
    context_object_name = 'Travel_Applications'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Travel_Application_list"] = Travel_Application.objects.all()
        context['Travel_ApplicationForm'] = Travel_ApplicationForm()
        return context
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")

    


class TravelApplicationView(ListView):
    model = Travel_Application
    template_name = 'Travel_Application/Travel_Application.html'
    context_object_name = 'Travel_Applications'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Travel_Application_list"] = Travel_Application.objects.filter(created_by=self.request.user.employee)
        context['Travel_ApplicationForm'] = Travel_ApplicationForm()

        return context

class Project_employee_assign_View(DetailView):
    model = Project_Employee_Assign
    template_name = 'pdf/employee_assign_pdf.html'
    context_object_name = 'project_employee_assign'
    pk_url_kwarg = 'id'  # This is where the 'id' parameter is mapped
        



class SalaryDetailView(UserPassesTestMixin,ListView):
    model = Salary
    template_name = 'Salary/SalarySingle.html'
    context_object_name = 'salary'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year, month, user = self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('user')
        context["year"] = self.kwargs.get('year')
        context["month"] = self.kwargs.get('month')
        context["user_id"] = self.kwargs.get('user')
        user_obj = Employee.objects.get(id=user)
        context["salary"] = Salary.objects.get(user=user, year=year, month=month)
        context["work_list"] = Clock.get_hour_for_month(user_obj,year,int(month))
        context["leave_details"] =Leave_Param.get_leave_param_all_details(user= user_obj,year=year,month=month)
        context["leave_cost_details"] =Leave_Param.get_year_total_cost_list(user= user_obj,year=year,month=month)
        job_money,job_food_money,Project_Job_Assign_details =  Project_Job_Assign.get_month_list_day(user_obj,year=year,month=month)
        Travel_Application_details_total_amount,Travel_Application_details_total_money,Travel_Application_details =  Travel_Application.get_time_cost_details_by_YM(user_obj,year=year,month=month)
        weekdays_overtime =  Work_Overtime_Application.get_money_by_user_month(user=user_obj,year=year,month=month)
        context["Project_Job_Assign_details"] = Project_Job_Assign_details
        context["job_money"] = job_money
        context["job_food_money"] = job_food_money
        context["Travel_Application_details"] = Travel_Application_details
        context["Travel_Application_details_total_amount"] = Travel_Application_details_total_amount
        context["Travel_Application_details_total_money"] = Travel_Application_details_total_money
        context["weekdays_overtime"] = weekdays_overtime

        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"薪水管理")


class SalaryListView(UserPassesTestMixin,ListView):
    model = Salary
    template_name = 'Salary/Salary.html'
    context_object_name = 'salaries'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        queryset = Salary.objects.filter(year=year, month=month)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        prev_month = month - 1
        prev_year = year

        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        context["year"] = year
        context["month"] = month
        next_month = month + 1
        next_year = year

        if next_month > 12:
            next_month = 1
            next_year += 1
        elif next_month < 1:
            next_month = 12
            next_year -= 1

        context["next_year"] = next_year
        context["next_month"] = next_month
        context["prev_year"] = prev_year
        context["prev_month"] = prev_month

        return context    
    def test_func(self):
        return Check_Permissions(self.request.user,"薪水管理")

    

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
        # verified用來判斷是否帳號密碼錯誤，要顯示資訊欄
        verified = False
        context = {
            'verified':verified,
        }
        return render(request, 'index/index-unlogin.html', context)
        

    def get(self,request):
      


        if not isinstance(request.user, AnonymousUser):
            # 使用者不是 AnonymousUser，代表是已登入的使用者
            # calculate_annual_leave()

            news = News.objects.all()
            employeeid = request.user.employee
            clock_inout = get_weekly_clock_data(employeeid)
            related_projects = Project_Job_Assign.objects.filter(lead_employee__in=[employeeid])|Project_Job_Assign.objects.filter(    work_employee__in=[employeeid]        )
            related_projects = related_projects.distinct()
            employee_assign_ids = Project_Job_Assign.get_assignments()


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

            work_list= Clock.get_hour_for_month(employeeid,date.today().year,date.today().month)

            
            context = {
                'clock_inout':clock_inout,
                'news':news,
                'work_list':work_list,
                "grouped_projects":sorted_grouped_projects,
                "employee_assign_ids":employee_assign_ids,
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
        context["employees_list"] = Employee.objects.values('id','full_name')
        context['client_list'] = Client.objects.all()
        context['project_confirmation_form'] = ProjectConfirmationForm()
        context['quotation_list'] = Quotation.objects.all()
        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"工程確認")

    


# 工作派任計畫
class Job_Assign_ListView(UserPassesTestMixin,ListView):
    model = Project_Job_Assign
    template_name = 'job_assign/job_assign.html'
    context_object_name = 'job_assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = Employee.objects.values('id','full_name')
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['project_job_assign_form'] = ProjectJobAssignForm()


        context['vehicle'] = Vehicle.objects.all()
        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"工程派任計畫")


# 派工單
class Employee_Assign_ListView(UserPassesTestMixin,ListView):
    model = Project_Employee_Assign
    template_name = 'employee_assign/employee_assign.html'
    context_object_name = 'Project_Employee_Assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] =  Employee.objects.values('id','full_name')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        context['vehicle'] = Vehicle.objects.all()
        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"工程派工單")

    

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
        return Check_Permissions(self.request.user,"管理部")

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
        return Check_Permissions(self.request.user,"管理部")

# 固定資產管理
class Equipment_ListView(UserPassesTestMixin,ListView):
    model = Equipment
    template_name = 'equipment/equipment.html'
    context_object_name = 'equipment'
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")
    


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
        context["employees_list"] =  Employee.objects.values('user__id','full_name') #用user_id 是要設計user的群組
        context['groups'] = sorted_groups
        return context
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部權限管理")



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
        return Check_Permissions(self.request.user,"管理部")       

# 基本資料(無法使用別人的id)
class Profile(DeleteView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    def get_object(self, queryset=None):
        # 從request.user中獲取當前用戶的id，然後返回相應的User物件
        return self.request.user


# 報價單
class Quotation_ListView(ListView):
    model = Quotation
    template_name = 'quotation/quotation.html'
    context_object_name = 'quotation'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workitems"]= Work_Item.objects.all()
        context['client'] = Client.objects.all()
        context['quotation'] = Quotation.objects.all().order_by("-id")
        from django.db.models import Case, When, Value, CharField
        employees_sorted = Employee.objects.annotate(#以業務組優先排序
            custom_order=Case(
                When(departments__department_name='業務組', then=Value(0)),
                default=Value(1)
            )
        ).order_by('custom_order')

        context['employees_sorted'] = employees_sorted
        print(employees_sorted  )

        return context
    
# 工項資料庫
class Work_Item_ListView(ListView):
    model = Work_Item
    template_name = 'work_item/work_item.html'
    context_object_name = 'work_item'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# 客戶管理
class Client_ListView(ListView):
    model = Client
    template_name = 'client/client.html'
    context_object_name = 'client_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# 車輛管理
class Vehicle_ListView(ListView):
    model = Vehicle
    template_name = 'vehicle/vehicle.html'
    context_object_name = 'vehicle_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["VehicleForm"] = VehicleForm
        return context
    
# 上班日調整
class ExtraWorkDay_ListView(UserPassesTestMixin,ListView):
    model = ExtraWorkDay
    template_name = 'extraworkday/extraworkday.html'
    context_object_name = 'extraworkday_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部管理")



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

#行事曆全
class Calendar_list(ListView):
    model = Employee
    template_name = 'calendar/calendar.html'
    context_object_name = 'employee'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all'] = 1
        return context



#申請單查詢
class Apply_List(View):
    template_name = 'apply_list/apply_list.html'

    @staticmethod
    def get_data():
        context = {
                "employees_list": Employee.objects.values('id', 'full_name'),
                "all_project_job_assign": Project_Job_Assign.objects.all(),
                "all_Equipment": Equipment.objects.all(),
                "project_confirmation_list": Project_Confirmation.objects.all(),
                "vehicle": Vehicle.objects.all(),
                "Travel_ApplicationForm": Travel_ApplicationForm(),
                "work_overtime_application_form": WorkOvertimeApplicationForm(),
                "leave_application_form": LeaveApplicationForm(),
                "clock_correction_application_form": ClockCorrectionApplicationForm(),
                "Project_location_list": Project_Job_Assign.objects.all(),
                "range_24": range(24),
                "range_60": range(60),
        }
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_data()
        return render(request, self.template_name, context)



    def post(self, request, *args, **kwargs):
        context = self.get_data()
        model_name = request.POST.get('model_name')
        obj_id = request.POST.get('obj_id',"")
        created_by = request.POST.get('created_by',"")
        if created_by:
            try:
                created_by = Employee.objects.get(full_name=created_by)
            except:
                context["error"]  = "找不到員工"
                return render(request, self.template_name, context)

        q_filter = Q()
        if obj_id:
            obj_id=int(obj_id)
            q_filter &= Q(id=obj_id)

        if created_by:
            q_filter &= Q(created_by=created_by)

        print(model_name, obj_id,created_by,q_filter)

        # 根據傳入的 model_name 選擇對應的模型 
        if model_name == 'work_overtime_application':
            model = Work_Overtime_Application
        elif model_name == 'leave_application':
            model = Leave_Application
        elif model_name == 'Travel_Application':
            model = Travel_Application
        elif model_name == 'clock_correction_application':
            model = Clock_Correction_Application
        elif model_name == 'all':
            pass
        else:
            context["error"]  = "錯誤類型"
            return render(request, self.template_name, context)
        
        models = []
        if model_name == 'all':
            work_overtime_objects = Work_Overtime_Application.objects.filter(q_filter).annotate(
                    model_url=Value("work_overtime_application")
                )
            leave_objects = Leave_Application.objects.filter(q_filter).annotate(
                model_url=Value("leave_application")
            )
            travel_objects = Travel_Application.objects.filter(q_filter).annotate(
                model_url=Value("Travel_Application")
            )
            clock_correction_objects = Clock_Correction_Application.objects.filter(q_filter).annotate(
                model_url=Value("clock_correction_application")
            )

            models += list(work_overtime_objects)
            models += list(leave_objects)
            models += list(travel_objects)
            models += list(clock_correction_objects)
        else:
            objects = model.objects.filter(q_filter).annotate(
                    model_url=Value(model_name)
            )
            models += list(objects)


        context["objects"] = models
        return render(request, self.template_name, context)

class Approval_List_Watch(UserPassesTestMixin,ListView):
    model = ApprovalModel
    template_name = 'approval_list/approval_list.html'
    context_object_name = 'approval_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = Employee.objects.values('id','full_name')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['vehicle'] = Vehicle.objects.all()
        context['Travel_ApplicationForm'] = Travel_ApplicationForm()
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["leave_application_form"] = LeaveApplicationForm()
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()
        context["Project_location_list"] = Project_Job_Assign.objects.all()
        context["24range"] = range(24)
        context["60range"] = range(60)
        return context

    def get_queryset(self):

        all_approval_models = ApprovalModel.objects.all().order_by("-id")

        related_approval_models = [
            approval_model for approval_model in all_approval_models
        ]
        queryset = related_approval_models
        return queryset
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")

    

class Approval_List(ListView):
    model = ApprovalModel
    template_name = 'approval_list/approval_list.html'
    context_object_name = 'approval_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = Employee.objects.values('id','full_name')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['vehicle'] = Vehicle.objects.all()
        context['Travel_ApplicationForm'] = Travel_ApplicationForm()
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["leave_application_form"] = LeaveApplicationForm()
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()
        context["Project_location_list"] = Project_Job_Assign.objects.all()
        context["24range"] = range(24)
        context["60range"] = range(60)
        return context

    def get_queryset(self):
        current_employee = self.request.user.employee

        all_approval_models = ApprovalModel.objects.all().order_by("-id")

        related_approval_models = [
            approval_model for approval_model in all_approval_models
            if approval_model.get_created_by == current_employee
        ]

        queryset = related_approval_models
        return queryset


class Approval_Process(ListView):
    model = ApprovalModel
    template_name = 'approval_process/approval_process.html'
    context_object_name = 'approval_process'

   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['Travel_ApplicationForm'] = Travel_ApplicationForm()
        context["employees_list"] = Employee.objects.values('id','full_name')
        context["all_project_job_assign"] = Project_Job_Assign.objects.all()
        context["all_Equipment"] = Equipment.objects.all()
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['vehicle'] = Vehicle.objects.all()        
        context["Project_location_list"] = Project_Job_Assign.objects.all()
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["leave_application_form"] = LeaveApplicationForm()
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)   

        current_employee = self.request.user.employee
    
        related_records = []        
        error_related_records = []        
        get_objs = ApprovalModel.objects.filter(current_status="in_process").order_by("-id")
        for Approval in get_objs:            
            try:
                get_employee = Approval.get_approval_employee() #看跟自己有沒有關係
                if get_employee !="x":
                    if  get_employee == current_employee :
                        related_records.append(Approval)
                else:
                    # 取得作者部門
                    get_createdby = Approval.get_created_by
                    print(Approval)
                    print(get_createdby)
                    department =get_createdby.departments
                    #撈取主管權限的員工
                    supervisor_employees = department.employees.filter(user__groups__name='主管').values_list('id', flat=True)
                    #判斷主管是不是在當前user
                    is_supervisor = current_employee.id in supervisor_employees
                    if is_supervisor:            
                        related_records.append(Approval)
            except:
                print("approval process error")
                error_related_records.append(Approval.id)
                continue
        context["related_records"] = related_records
        context["error_related_records"] = error_related_records

        return context
    

    

# 簽核順序
class Approval_Group(UserPassesTestMixin,ListView):
    model = Approval_Target
    template_name = 'approval_group/approval_group.html'
    context_object_name = 'approval_group'

    def test_func(self):
        return Check_Permissions(self.request.user,"簽核流程管理")

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
        return Check_Permissions(self.request.user,"管理部管理")

# 請假申請

class Leave_Application_Watch_List(UserPassesTestMixin,ListView):
    model = Leave_Application
    template_name = 'leave_application/leave_application_watch.html'
    context_object_name = 'leave_application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leave_application_form"] = LeaveApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        context["leave_application_list"] =Leave_Application.objects.all()
        return context
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")



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
        current_year = datetime.now().year
        context["leave_details"] =Leave_Param.get_leave_param_all_details(user,year=current_year)
        context["leave_application_list"] =Leave_Application.objects.filter(created_by=user)
        return context


# 加班申請
class Work_Overtime_Application_List(ListView):
    model = Work_Overtime_Application
    template_name = 'work_overtime_application/work_overtime_application.html'
    context_object_name = 'work_overtime_application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.employee
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        context["work_overtime_application_list"] =Work_Overtime_Application.objects.filter(created_by=user)
        return context
    
class Work_Overtime_Application_Watch_List(UserPassesTestMixin,ListView):
    model = Work_Overtime_Application
    template_name = 'work_overtime_application/work_overtime_application_watch.html'
    context_object_name = 'work_overtime_application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.employee
        context["work_overtime_application_form"] = WorkOvertimeApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        context["work_overtime_application_list"] =Work_Overtime_Application.objects.all()
        return context

    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")

    

# 補卡申請

class Clock_Correction_Application_Watch_List(UserPassesTestMixin,ListView):
    model = Clock_Correction_Application
    template_name = 'clock_correction_application/clock_correction_application_watch.html'
    context_object_name = 'clock_correction_applications'

    def get_context_data(self, **kwargs):
        user = self.request.user.employee
        context = super().get_context_data(**kwargs)
        context["clock_correction_application_list"] =Clock_Correction_Application.objects.filter()
        context["clock_correction_application_form"] = ClockCorrectionApplicationForm()
        context["24range"] = range(24)
        context["60range"] = range(60)
        return context
    
    def test_func(self):
        return Check_Permissions(self.request.user,"管理部")




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
    


