from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from Backend.forms import  ProjectForm, ProjectConfirmationForm
from Backend.models import Department, Project_Confirmation,Employee
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy


# 首頁
class Index(View):

    def post(self,request):
        # login_form = LoginForm()
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
                    print("Save")
                    print(session)
                    session.save()
                return HttpResponseRedirect('/')

    def get(self,request):
        return render(request, 'index/index.html')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


# 工程確認單，使用 ListView 顯示資料而已，做表單送出都在 Backend 的 Views.py
class Project_Confirmation(ListView):
    model = Project_Confirmation
    template_name = 'project_confirmation/project_confirmation.html'
    context_object_name = 'project_confirmation'
    # current_usera="5121"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["employees_list"] =employees = Employee.objects.values('id','user__username')
        print(context)
        return context

    # def get(self,request):    
        # return render(request, 'project_confirmation/project_confirmation.html')

# 工作派任計畫
class Project(ListView):

    def put(self, request):#未測試
        project = get_object_or_404(Project, pk=request.POST['project_id'])
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()
        else:
            error_messages = form.get_error_messages()
            print(error_messages)

        return HttpResponseRedirect(request.path)

    def post(self,request):
        #目前前端html，只有工作地點有name!
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save() 
        else:
            error_messages = form.get_error_messages()
            print(error_messages)

        return HttpResponseRedirect(request.path)


    def get(self,request):    
        context = {
            'form': ProjectForm,
        }
        return render(request, 'project/project.html', context)

@login_required
def equipment(request):
    context = {
        
    }
    return render(request, 'equipment/equipment.html', context)

class Department(ListView):
    model = Department
    template_name = 'department/department.html'
    context_object_name = 'department'

    def post(self,request):
      
        for key, value in request.POST.items():
            # 对每个字段执行相应的操作
            print(f"字段名: {key}, 值: {value}")

        context = {
            
        }
        return render(request, 'department/department.html', context)
    
    # CBV 要取得物件好像要使用 ListView，ListView 就不判斷 get、post，加上 get 會影響吃不到上面寫的 model
    # def get(self,request):
    #     context = {
    #     }
    #     return render(request, 'department/department.html', context)


def menu_item(request, menu_item):


    context = {
        'menu_item': menu_item,
        # 'form':get_form(menu_item)
        
    }
    return render(request, 'index/index.html', context)