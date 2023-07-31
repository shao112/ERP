from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed,HttpResponseRedirect,HttpResponse
import json
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.db import models
from django.db.models.fields.files import FieldFile
from django.db.models.fields.related import ManyToManyField
from django.core.exceptions import ObjectDoesNotExist

from Backend.models import Department, Project_Confirmation, Employee, Project_Job_Assign,News,Clock,Project_Employee_Assign
from django.contrib.auth.models import User,Group
from Backend.forms import  ProjectConfirmationForm, GroupForm, EmployeeForm, ProjectJobAssignForm,NewsForm,Project_Employee_AssignForm
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from .utils import convent_dict,convent_employee,convent_excel_dict,match_excel_content
import openpyxl
from django.db.utils import IntegrityError
import random
import os
from  django.conf import settings

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

class Project_Employee_Assign_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = Project_Employee_AssignForm(dict_data)
        if form.is_valid():
            get_Project_Employee_Assign =Project_Employee_Assign.objects.get(id=dict_data['id'])

            if "project_job_assign" in dict_data:
                project_job_assign_instance = Project_Job_Assign.objects.get(pk=int(dict_data["project_job_assign"]))
                get_Project_Employee_Assign.project_job_assign = project_job_assign_instance            
                del dict_data["project_job_assign"]

            get_Project_Employee_Assign.update_fields_and_save(**dict_data)

            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)  
            Project_Employee_Assign.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:        
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:        
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = Project_Employee_AssignForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({"data":"新增成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Project_Employee_Assign, id=id)
        data = model_to_dict(data)
        data["inspector"] = convent_employee(data["inspector"])
        print(data)
        if  data['enterprise_signature']:
            data['enterprise_signature'] = data['enterprise_signature'].url
        else:
            data['enterprise_signature'] = None            
        print("dict_data")
        print(data)
        return JsonResponse({"data":data}, status=200,safe = False)

class New_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = NewsForm(dict_data)
        if form.is_valid():
            News.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)  
            News.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:        
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:        
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = NewsForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({"data":"新增成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(News, id=id)
        data = model_to_dict(data)
        print("dict_data")
        print(data)
        return JsonResponse({"data":data}, status=200,safe = False)



class IMGUploadView(View):
    def post(self, request):
        image_file = request.FILES.get('upload_img')
        if image_file !=None:
            random_number = str(random.randint(1, 99))
            new_file_name = f"{random_number}_{image_file.name}"
            file_path = rf'{settings.MEDIA_ROOT}/news_uploads/{new_file_name}'

            with open(file_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            return JsonResponse({"url":f"/media/news_uploads/{new_file_name}"},status=200)

        return HttpResponse(status=500)




class FileUploadView(View):
   def post(self, request, *args, **kwargs):
        modelstr = self.kwargs['model']
        uploaded_file = request.FILES.get('fileInput')

        if uploaded_file ==None:
             return JsonResponse({'error': '請上傳檔案'}, status=500)
        #檢查type，回傳上傳正確檔案

        workbook = openpyxl.load_workbook(uploaded_file)
        worksheet = workbook.active
        get_dicts,get_model = convent_excel_dict(worksheet,modelstr)
        error_str=""
        print(get_dicts)
        for i,get_dict in enumerate(get_dicts):
            try:
                 get_model.objects.create(**get_dict)
            except IntegrityError as e: #錯誤發生紀錄，傳給前端
                error_str=f"第{i+1}欄資料錯誤\n"

        if error_str=="":
            return JsonResponse({'message': '上傳成功'},status=200)
        else:
            return JsonResponse({'error': '上傳失敗欄為:'}, status=500)



class Groups_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        group = Group.objects.get(id=dict_data['id'])
        user_ids= dict_data["user_set"]
        users = User.objects.filter(id__in=user_ids)       
        group.user_set.set(users)   
        return JsonResponse({'data': "修改成功"},status=200)

    def get(self, request):
        id = request.GET.get('id')
        data = get_object_or_404(Group, id=id)
        groups_employee = data.user_set.all()
        users = [user.id for user in groups_employee]
        data={"user_set":users,"id":data.id,"group_name":data.name}

        return JsonResponse({"data": data}, status=200)

class Profile_View(View):
    # 同一個post要處理更新照片以及更新密碼
    def post(self,request):
        print("Profile_View")
        if 'profile_image' in request.FILES:
            uploaded_image = request.FILES.get('profile_image')
            employee = get_object_or_404(Employee, id=request.user.employee.id)
            print(employee.profile_image.path)
            print(employee)
            now = datetime.now()
            date_time_string = now.strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(uploaded_image.name)[1]
            new_file_name = f"{date_time_string}{file_extension}"
            employee.profile_image.save(new_file_name, uploaded_image)
            print("成功")
            return JsonResponse({'status': 'success'},status=200)
        else:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return JsonResponse({'status': 'success'},status=200)
            else:
                return JsonResponse({"data":form.errors}, status=400,safe=False)
        
    # def put(self,request):
    #     print("views.py put")
    #     uploaded_image = request.FILES.get('profile_image')
    #     print(uploaded_image)
    #     if uploaded_image == None:
    #          return JsonResponse({'error': '請上傳檔案'}, status=400)
    #     else:
            # employee = Employee.objects.filter(pk=request.user.id).update(profile_image=uploaded_image)
            # employee.save()
            # return JsonResponse(status=200)



class Employee_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = EmployeeForm(dict_data)
        if form.is_valid():               
            getObject=Employee.objects.get(id=dict_data['id'])
            if "departments" in dict_data:
                Department_instance = Department.objects.get(pk=int(dict_data["departments"]))
                getObject.departments = Department_instance            
                del dict_data["departments"]
            else:
                getObject.departments = None

            getObject.update_fields_and_save(**dict_data)
            return JsonResponse({'data': "完成新增"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)  
            empolyee = Employee.objects.get(id=dict_data['id'])
            empolyee.user.is_active =False
            empolyee.user.save()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:        
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:        
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = EmployeeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['full_name']
            password = form.cleaned_data['id_number']
            user = User.objects.create_user(username=username, password=password)
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            return JsonResponse({'data': "完成新增"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Employee, id=id)
        data = model_to_dict(data)
        return JsonResponse({"data":data}, status=200,safe = False)





class Project_Confirmation_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)  
        form = ProjectConfirmationForm(dict_data)
        if form.is_valid():
            getObject = Project_Confirmation.objects.get(id=dict_data['id'])
            if "completion_report_employee" in dict_data:
                get_completion_report_employee = dict_data["completion_report_employee"]
                del dict_data["completion_report_employee"]
                getObject.completion_report_employee.set(get_completion_report_employee)

            getObject.update_fields_and_save(**dict_data)

            return JsonResponse({'data': "完成修改"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)  
            Project_Confirmation.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:        
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:        
            print(e)
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = ProjectConfirmationForm(request.POST)

        if form.is_valid():
            form.save() 
            return JsonResponse({'data': "完成新增"},status=200)
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Project_Confirmation, id=id)
        data = model_to_dict(data) 
        data["completion_report_employee"] = convent_employee(data["completion_report_employee"])
        if  data['reassignment_attachment']:
            data['reassignment_attachment'] = data['reassignment_attachment'].url
        else:
            data['reassignment_attachment'] = None            
        return JsonResponse({"data":data}, status=200,safe = False)

class Job_Assign_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)  
        form = ProjectJobAssignForm(dict_data)
        if form.is_valid():
            getObject = Project_Job_Assign.objects.get(id=dict_data['id'])
            process_key =("support_employee","work_employee","lead_employee","project_confirmation")

            for key in process_key:#處理特別key
                if key in dict_data:
                    if key == "project_confirmation":
                        confirmation_instance = Project_Confirmation.objects.get(pk=int(dict_data["project_confirmation"]))
                        getObject.project_confirmation = confirmation_instance                   
                    else:
                        field = getattr(getObject, key)
                        field.set(dict_data[key])

            for key in process_key:#刪除處理完的key
                if key in dict_data:
                    del dict_data[key]

            getObject.update_fields_and_save(**dict_data)

            return JsonResponse({'data': "完成修改"},status=200)
        else:
            return JsonResponse({"error":form.errors},status=400)

    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)  
            Project_Job_Assign.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:        
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:        
            print(e)
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = ProjectJobAssignForm(request.POST)

        if form.is_valid():
            form.save() 
            return JsonResponse({'data':"完成新增"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):        
        id = request.GET.get('id')
        data = get_object_or_404(Project_Job_Assign, id=id)
        print(data)


        #渲染關聯
        selected_fields = ['quotation_id', 'project_name', 'client', 'requisition']
        project_confirmation_dict = model_to_dict(data.project_confirmation, fields=selected_fields)

        data = model_to_dict(data)
        data["lead_employee"] = convent_employee(data["lead_employee"])
        data["work_employee"] = convent_employee(data["work_employee"])

        data['project_confirmation'] = project_confirmation_dict

        if  "attachment" in data:
            if  data['attachment']:
                data['attachment'] = data["attachment"].url
            else:
                data['attachment'] = None            
        return JsonResponse({"data":data,"project_confirmation":project_confirmation_dict}, status=200,safe = False)



class ExcelExportView(View):
   def get(self, request, *args, **kwargs):
        modelstr = self.kwargs['model']
        match_excel_content(modelstr)
        project_confirmation_list = Project_Confirmation.objects.all()
        wb = openpyxl.Workbook()
        ws = wb.active
        # 1.排除掉不要的欄位
        exclude_fields = ['project','id','author','modified_by','created_date','update_date']
        # 2.取得原欄位名
        field_names = [field.name for field in Project_Confirmation._meta.get_fields() if isinstance(field, models.Field) and field.name not in exclude_fields]
        # 3.透過原欄位名取得欄位名的verbose name
        fields_with_verbose_names = {
            field_name: Project_Confirmation._meta.get_field(field_name).verbose_name for field_name in field_names
        }
        # 4.fields_with_verbose_names是dict，要轉成[]才能ws.append()
        header_rows = []
        for field_name, verbose_name in fields_with_verbose_names.items():
            header_rows.append(verbose_name)
        ws.append(header_rows)
        
        # 要排除掉特殊欄位
        # for article in project_confirmation_list:
        #     # row_data = [getattr(article, field) for field in field_names]
        #     row_data = [getattr(article, field).name if isinstance(getattr(article, field), FieldFile) else getattr(article, field) for field in field_names]

        #     print(row_data)
        #     ws.append(row_data)
        # 将所有文章数据写入Excel
        # for project_confirmation in project_confirmation_list:
        #     ws.append([project_confirmation.project_confirmation_id, project_confirmation.quotation_id, project_confirmation.project_name])
        for article in project_confirmation_list:
            row_data = []
            for field_name in field_names:
                field = Project_Confirmation._meta.get_field(field_name)
                if isinstance(field, ManyToManyField):
                    # 处理多对多关系的字段，拼接为一个字符串
                    related_objects = getattr(article, field_name).all()
                    field_value = ', '.join(str(obj) for obj in related_objects)
                else:
                    # 处理其他普通字段
                    field_value = getattr(article, field_name)
                    if isinstance(field_value, FieldFile):
                        field_value = field_value.url if field_value else ''
                print(field_value)
                row_data.append(field_value)
                # field_value = getattr(article, field_name)
                # if not isinstance(field_value, (FieldFile,ManyToManyField)):
                #     row_data.append(field_value)

                #     print(row_data)
            ws.append(row_data)

        # 设置响应头，指定导出文件的类型和名称
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=articles.xlsx'

        # 将Excel数据保存到响应中
        wb.save(response)

        return response
   

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

        return JsonResponse({'status': 'success'},status=200)

    def get(self,request):        
       return HttpResponseNotAllowed(['only POST'])
    
