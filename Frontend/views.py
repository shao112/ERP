from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required

from Backend.forms import  ProjectConfirmationForm, EmployeeForm, NewsForm
from Backend.models import User, Department, Project_Job_Assign, Project_Confirmation,Project_Employee_Assign,Employee, News, Equipment, Vehicle
from django.views.generic import ListView, DeleteView


from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date
from django.views.defaults import permission_denied
from Backend.utils import convent_employee,get_weekly_clock_data
from django.db.models import Q

def custom_permission_denied(request, exception=None,template_name='403.html'):
    return permission_denied(request, exception, template_name='403.html')



def testpdf1(request):  
    import pdfkit
    from django.http import HttpResponse



    url = "http://localhost:8000/watch"  # Replace with the actual URL
    pdf_file_path = "output.pdf"

    # Generate PDF from the URL
    # pdfkit.from_string('Thanks for reading!', 'out3.pdf')
    # pdf = HTML(url).write_pdf()
    # print("xxxx")
    # from pyhtml2pdf import converter
    # converter.convert("https://en.wikipedia.org/wiki/Elon_Musk", pdf_file_path)
    import pdfkit 
    pdfkit.from_url('https://www.google.com/',pdf_file_path) 
    print("xxxx")
    print("xxxx")

    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    return response    

def testpdf(request):

    def fetch_resources(uri, rel):
        from django.conf import settings
        path = settings.BASE_DIR + uri
        return path
    
    def link_callback(uri):
        from django.conf import settings
        import os
        if uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace(settings.MEDIA_URL, ""))
        elif uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT,
                                uri.replace(settings.STATIC_URL, ""))
        else:
            return uri

        # 确保本地文件存在
        if not os.path.isfile(path):
            raise Exception(
                "Media URI 必须以以下格式开头"
                f"'{settings.MEDIA_URL}' or '{settings.STATIC_URL}'")

        return path
    
        # from xhtml2pdf import pisa

    def generate_pdf(project_employee_assign_id):
        from django.template.loader import get_template,render_to_string
        from django.http import HttpResponse
        from io import BytesIO  # 導入 BytesIO 類別
        from xhtml2pdf import pisa

        project_employee_assign = Project_Employee_Assign.objects.get(pk=project_employee_assign_id)
        template_path = 'pdf/Equipment_pdf.html' 
        context = {'project_employee_assign': project_employee_assign}


        pdf_buffer = BytesIO()
        htmltemplate = render_to_string(template_path,context)
        pdf = pisa.CreatePDF(htmltemplate, pdf_buffer,link_callback=fetch_resources, encoding='utf-8')


        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="project_assignment_{project_employee_assign_id}.pdf"'
        return response

    # return generate_pdf(3)
    project_employee_assign = Project_Employee_Assign.objects.get(id=2)
    context={
        "project_employee_assign":project_employee_assign,
    }
    return render(request, 'pdf/Equipment_pdf.html',context)    

# 首頁
class Director_Index(View):
    def get(self,request):
            current_employee = request.user.employee
            
            other_employees = current_employee.departments.employees.exclude(id=current_employee.id)
            other_employees = convent_employee(other_employees)
            for employee in other_employees:
                employee['clock_data'] = get_weekly_clock_data(employee['id'])

            print(other_employees)
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
        # 0710
        # 以下寫法: employeeid = request.user.employee
        # 這樣寫出現問題: 我們登入登出頁面都做在一起，當登出時，也會跑來此get()，而user會變成AnonymousUser，AnonymousUser裡面不存在employee，頁面壞掉
        # (Django做使用者登出時，request.user變成AnonymousUser是預設行為)
        # 目前先加上判斷是不是AnonymousUser，再觀察有沒有效

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
                    for date_str in project.attendance_date:
                        date_obj = date.fromisoformat(date_str)
                        print(date_obj)
                        print( date.today())
                        if date_obj >= date.today():
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


class Project_Confirmation_ListView(UserPassesTestMixin,ListView):
    model = Project_Confirmation
    template_name = 'project_confirmation/project_confirmation.html'
    context_object_name = 'project_confirmation'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["employees_list"] = Employee.objects.values('id','user__username')
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='工程部總管理').exists()    
    


# 工作派任計畫
class Job_Assign_ListView(ListView):
    model = Project_Job_Assign
    template_name = 'job_assign/job_assign.html'
    context_object_name = 'job_assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context['project_confirmation_list'] = Project_Confirmation.objects.all()
        context['vehicle'] = Vehicle.objects.all()
        return context

# 派工單
class Employee_Assign_ListView(ListView):
    model = Project_Employee_Assign
    template_name = 'employee_assign/employee_assign.html'
    context_object_name = 'Project_Employee_Assign'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees_list"] = employee = Employee.objects.values('id','user__username')
        context["all_project_job_assign"] = Project_Job_Assign.objects.values('id','project_confirmation__project_confirmation_id')
        context["all_Equipment"] = Equipment.objects.all()
        return context


    

# 員工
class Employee_list(ListView):
    model = Employee
    template_name = 'employee/employee.html'
    context_object_name = 'employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department_list"] = Department.objects.values('id','department_name')
        context['employee_form'] = EmployeeForm()
        return context

# 員工出勤
class Employee_Attendance_list(ListView):
    model = Employee
    template_name = 'employee_attendance/employee_attendance.html'
    context_object_name = 'employees'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        return context

# 固定資產管理
class Equipment_ListView(ListView):
    model = Equipment
    template_name = 'equipment/equipment.html'
    context_object_name = 'equipment'

    


from django.contrib.auth.models import Group
# 員工權限
class Employee_Permission_list(ListView):
    model = Employee
    template_name = 'employee_permission/employee_permission.html'
    context_object_name = 'employees'
    def get_context_data(self, **kwargs):
        Groups = Group.objects.all()
        context = super().get_context_data(**kwargs)
        context["employees_list"] =  Employee.objects.values('user__id','user__username')
        context['groups'] = Groups
        return context
    


class Department_list(ListView):
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

# 基本資料(無法使用別人的id)
class Profile(DeleteView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    def get_object(self, queryset=None):
        # 從request.user中獲取當前用戶的id，然後返回相應的User物件
        return self.request.user

# 最新消息
class News_ListView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_form'] = NewsForm()
        return context
# 最新消息
class Calendar(ListView):
    model = Employee
    template_name = 'calendar/calendar.html'
    context_object_name = 'employee'