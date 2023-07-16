from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed,HttpResponseRedirect
import json
from datetime import datetime

from .models import Clock
from Backend.models import Department, Project_Confirmation, Employee, Project_Job_Assign
from django.contrib.auth.models import User,Group
from Backend.forms import  ProjectConfirmationForm, GroupForm, EmployeeForm, ProjectJobAssignForm

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from .utils import convent_dict
import datetime

class Groups_View(View):

    def delete(self,request):
        dict_data = convent_dict(request.body)
        group = Group.objects.get(id=dict_data['id'])
        print("put")
        print(dict_data)
        for userid in dict_data["user_set"]:
            user = User.objects.get(id=userid)
            user.groups.remove(group)
        return JsonResponse({'status': 200})


    def put(self,request):
        dict_data = convent_dict(request.body)
        group = Group.objects.get(id=dict_data['id'])
        print("put")
        print(dict_data)
        for userid in dict_data["user_set"]:
            user = User.objects.get(id=userid)
            user.groups.add(group)
        return JsonResponse({'status': 200})


    def post(self,request):
        pass

    def get(self, request):
        id = request.GET.get('id')
        data = get_object_or_404(Group, id=id)
        groups_employee = data.user_set.all()
        users = [user.id for user in groups_employee]
        data={"user_set":users,"id":data.id}

        return JsonResponse({"data": data, "status": 200}, status=200)

class Check(View):
    def post(self,request):
        data = json.loads(request.body)
        gps = data.get('gps')
        clock_in_or_out = data.get('clock_in_or_out')
        clock_time = datetime.datetime.now()

        Clock.objects.create(
            employee_id=request.user.employee,
            clock_time=clock_time,
            clock_in_or_out=clock_in_or_out,
            clock_GPS=gps
        )

        return JsonResponse({'status': 'success'})

    def get(self,request):        
       return HttpResponseNotAllowed(['only POST'])
    



class Employee_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = EmployeeForm(dict_data)
        if form.is_valid():
            Employee.objects.filter(id=dict_data['id']).update(**dict_data)
            return JsonResponse({'status': 200})
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({'status': 400,"error":error_messages})

    
    def delete(self,request):
        dict_data = convent_dict(request.body)  
        empolyee = Employee.objects.get(id=dict_data['id'])
        empolyee.user.is_active =False
        empolyee.user.save()
        return JsonResponse({'status': 200})

    def post(self,request):
        form = EmployeeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['full_name']
            password = form.cleaned_data['id_number']
            user = User.objects.create_user(username=username, password=password)
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            return JsonResponse({'status': 200})
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({'status': 400,"error":error_messages})


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Employee, id=id)
        data = model_to_dict(data)
        return JsonResponse({"data":data,"status":200}, status=200,safe = False)





class Project_Confirmation_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)  
        form = ProjectConfirmationForm(dict_data)
        if form.is_valid():
            Project_Confirmation.objects.filter(id=dict_data['id']).update(**dict_data)
            return JsonResponse({'status': 200})
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({'status': 400,"error":error_messages})

    
    def delete(self,request):
        dict_data = convent_dict(request.body)  
        Project_Confirmation.objects.get(id=dict_data['id']).delete()

        return JsonResponse({'status': 200})

    def post(self,request):
        form = ProjectConfirmationForm(request.POST)

        if form.is_valid():
            form.save() 
            return JsonResponse({'status': 200})
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({'status': 400,"error":error_messages})


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Project_Confirmation, id=id)
        data = model_to_dict(data)  
        if  data['reassignment_attachment']:
            data['reassignment_attachment'] = data['reassignment_attachment'].url
        else:
            data['reassignment_attachment'] = None            
        return JsonResponse({"data":data,"status":200}, status=200,safe = False)

class Job_Assign_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)  
        form = ProjectJobAssignForm(dict_data)
        if form.is_valid():
            Project_Job_Assign.objects.filter(id=dict_data['id']).update(**dict_data)
            return JsonResponse({'status': 200})
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({'status': 400,"error":error_messages})

    
    def delete(self,request):
        dict_data = convent_dict(request.body)  
        Project_Job_Assign.objects.get(id=dict_data['id']).delete()

        return JsonResponse({'status': 200})

    def post(self,request):
        form = ProjectJobAssignForm(request.POST)

        if form.is_valid():
            form.save() 
            return JsonResponse({'status': 200})
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({'status': 400,"error":error_messages})


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Project_Job_Assign, id=id)
        data = model_to_dict(data)
        if  "reassignment_attachment" in data:
            if  data['reassignment_attachment']:
                data['reassignment_attachment'] = data.url
            else:
                data['reassignment_attachment'] = None            
        return JsonResponse({"data":data,"status":200}, status=200,safe = False)

