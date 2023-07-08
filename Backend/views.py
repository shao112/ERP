from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed
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

class Project_Confirmation_View(View):
    def put(self,request):
        print("修改")
        data = request.body  
        data_str = data.decode('utf-8')
        json_data = parse_qs(data_str)
        json_data = {key: value[0] for key, value in json_data.items()}
        del  json_data["csrfmiddlewaretoken"]
        print(json_data)
        form = ProjectConfirmationForm(json_data)

        if form.is_valid():
            #可能要用update
            # form.save() 
            return JsonResponse({'status': 200})
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({'status': 400,"error":error_messages})

    
    def delete(self,request):
        #未做
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

