from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed,HttpResponseRedirect
import json
from datetime import datetime
from Backend.models import Department, Project_Confirmation
from .models import Clock
from Backend.forms import   ProjectConfirmationForm
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

class Check(View):
    def post(self,request):
        data = json.loads(request.body)
        gps = data.get('gps')
        clock_in_or_out = data.get('clock_in_or_out')
        clock_time = data.get('clock_time')
        clock_time = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%fZ')

        Clock.objects.create(
            employee_id=request.user.employee,
            clock_time=clock_time,
            clock_in_or_out=clock_in_or_out,
            clock_GPS=gps
        )

        return JsonResponse({'status': 'success'})

    def get(self,request):        
       return HttpResponseNotAllowed(['only POST'])
    

from urllib.parse import parse_qs

def convent_dict(data):
    data_str = data.decode('utf-8')
    dict_data = parse_qs(data_str)
    new_dict_data = {}
    for key, value in dict_data.items():
        new_dict_data[key] = value[0]
        match  value[0]:
            case "true":
                new_dict_data[key] = True
            case "false":
                new_dict_data[key] =False
            case _:
                new_dict_data[key] = value[0]
    del  new_dict_data  ["csrfmiddlewaretoken"]    
    return new_dict_data

class Project_Confirmation_View(View):

    def put(self,request):
        print("修改")
        dict_data = convent_dict(request.body)  
        form = ProjectConfirmationForm(dict_data)
        if form.is_valid():
            Project_Confirmation.objects.filter(id=dict_data['id']).update(**dict_data)
            return JsonResponse({'status': 200})
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({'status': 400,"error":error_messages})

    
    def delete(self,request):
        print("刪除")
        data = request.body 
        data_str = data.decode('utf-8')
        json_data = parse_qs(data_str)
        json_data = {key: value[0] for key, value in json_data.items()}
        # del  json_data["csrfmiddlewaretoken"]
        print(json_data)
        project_confirmation = Project_Confirmation.objects.get(id=json_data['id'])
        project_confirmation.delete()

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
        print(request)
        id = request.GET.get('id')
        data = get_object_or_404(Project_Confirmation, id=id)
        data = model_to_dict(data)
        if  data['reassignment_attachment']:
            data['reassignment_attachment'] = data.url
        else:
            data['reassignment_attachment'] = None            

        # json_data = json.dumps(data, cls=DjangoJSONEncoder)

        return JsonResponse({"data":data,"status":200}, status=200,safe = False)

