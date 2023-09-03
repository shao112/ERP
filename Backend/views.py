from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed,HttpResponseRedirect,HttpResponse,Http404
import json
import datetime
from django.contrib.auth import update_session_auth_hash
import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from Backend.models import SysMessage,Approval_Target, Equipment, UploadedFile,Department,Quotation,ApprovalLog,Work_Item,ApprovalModel, Project_Confirmation, Employee, Project_Job_Assign,News,Clock,Project_Employee_Assign
from django.contrib.auth.models import User,Group
from Backend.forms import   ProjectConfirmationForm,EquipmentForm,QuotationForm,DepartmentForm,Work_ItemForm,  EmployeeForm, ProjectJobAssignForm,NewsForm,Project_Employee_AssignForm
from django.contrib.auth.forms import PasswordChangeForm
from urllib.parse import parse_qs

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from .utils import convent_dict,convent_employee,convent_excel_dict,match_excel_content,get_model_by_name
import openpyxl
from openpyxl.utils import get_column_letter
from django.db.utils import IntegrityError
import random
import os
import re


from  django.conf import settings

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.utils.text import get_valid_filename # 確保file檔名是合法的，不接受的符號會轉成可接受符號




class SysMessage_API(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        id = data.get('id')  # 获取 id
        getobj = SysMessage.objects.get(id=id)
        getobj.watch=True
        getobj.save()
        return HttpResponse(200)

class Approval_View_Process(View):
    def post(self,request):
        try:
            id = request.POST.get('id')
            modeltext = request.POST.get('model')

            getmodel = get_model_by_name(modeltext)
            if getmodel is  None:
                return JsonResponse({"error":"找不到model"},status=400)

            try:
                get_obj = get_object_or_404(getmodel, id=id)
            except Http404:
                return JsonResponse({"error": "找不到相應的ID obj"}, status=404)
            
            model_name = {
                'project_confirmation': 'Project_Confirmation',
                'job_assign': 'Project_Job_Assign',
                'project_employee_assign': 'Project_Employee_Assign',
                '請假單': '請假單',
            }

            try:
                get_Approval_Target = get_object_or_404(Approval_Target, name=model_name.get(modeltext))
            except Http404:
                return JsonResponse({"error": "找不到相應的簽核目標"}, status=404)

            new_Approval= ApprovalModel.objects.create(target_approval=get_Approval_Target)
            get_obj.Approval=new_Approval
            get_obj.save()
            return JsonResponse({"success":"成功"},status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": f"系統發生錯誤, {str(e)} "}, status=500)

    def delete(self,request):
        data = request.body.decode('utf-8')
        parsed_data = parse_qs(data)
        id = parsed_data.get('id', [None])[0]
        modeltext = parsed_data.get('model', [None])[0]
        getmodel = get_model_by_name(modeltext)

        if getmodel is  None:
            return JsonResponse({"error":"找不到model"},status=400)

        try:
            get_obj = get_object_or_404(getmodel, id=id)
        except Http404:
            return JsonResponse({"error": "找不到相應的ID obj"}, status=404)
        
        user = request.user.employee
        approval_obj = get_obj.Approval

        if approval_obj.current_status == 'in_progress':
            approval_obj.send_message_to_related_users(f"{get_obj.get_show_id()} 單被{user.full_name}收回簽核")
            approval_obj.delete()

            return JsonResponse({"message": "删除成功"}, status=200)
        elif approval_obj.current_status == 'completed':
            if request.user.groups.filter(name='主管').exists():
                approval_obj.send_message_to_related_users(f"{get_obj.get_show_id()} 單被{user.full_name}收回簽核")
                approval_obj.delete()
                # get_obj.Approval=None
                # get_obj.save()
                return JsonResponse({"message": "删除成功"}, status=200)
            else:
                return JsonResponse({"error": "只有主管才可處理"}, status=403)
        else:
            return JsonResponse({"error": "操作不允許"}, status=403)
 


class Approval_Process_Log(View):
    def post(self,request):
        status = request.POST.get('status')
        feedback = request.POST.get('feedback')
        approval_id = request.POST.get('Approval_id')

        if status not in ["approved", "rejected"]:
            return JsonResponse({"error":"請選擇簽核狀態"},status=400)
        
        if approval_id ==None: 
            return JsonResponse({"error":"請選擇approval"},status=400)
        
        #尋找實體
        try:
            approval_instance = get_object_or_404(ApprovalModel, id=approval_id)
        except Http404:
            return JsonResponse({"error": "找不到相應的ApprovalModel"}, status=404)

        ApprovalLog.objects.create(
            approval=approval_instance,
            user=request.user.employee,
            content=feedback,
        )
        approval_instance.update_department_status(status)
        
        if status:
            return JsonResponse({"data":"ok"},status=200)

class Department_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = DepartmentForm(dict_data)
        if form.is_valid():

            get_object=Department.objects.get(id=dict_data['id'])
            if "parent_department" in dict_data:
                Equipment_nstance = Department.objects.get(pk=int(dict_data["parent_department"]))
                get_object.parent_department = Equipment_nstance
                del dict_data["parent_department"]
            
            get_object.update_fields_and_save(**dict_data)

            Department.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Department.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = DepartmentForm(request.POST)

        if form.is_valid():
            newobj =form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Department, id=id)
        data = model_to_dict(data)

        return JsonResponse({"data":data}, status=200,safe = False)


class Equipment_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)

        form = EquipmentForm(dict_data)
        if form.is_valid():
            Equipment.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Equipment.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = EquipmentForm(request.POST)

        if form.is_valid():
            newobj =form.save()

            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Equipment, id=id)
        data = model_to_dict(data)
        data['abnormal_img'] = data['abnormal_img'].url if data['abnormal_img']   else ''
        data['buy_img'] = data['buy_img'].url if data['buy_img']  else ''
        print("dict_data")
        print(data)
        return JsonResponse({"data":data}, status=200,safe = False)


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

            if "carry_equipments" in dict_data:
                get_carry_equipments = dict_data["carry_equipments"]
                get_carry_equipments = [int(item) for item in get_carry_equipments]
                print(get_carry_equipments)
                del dict_data["carry_equipments"]
                get_Project_Employee_Assign.carry_equipments.set(get_carry_equipments)

            if "lead_employee" in dict_data:
                get_completion_report_employee = dict_data["lead_employee"]
                del dict_data["lead_employee"]
                get_Project_Employee_Assign.lead_employee.set(get_completion_report_employee)

            if "inspector" in dict_data:
                get_completion_report_employee = dict_data["inspector"]
                del dict_data["inspector"]
                get_Project_Employee_Assign.inspector.set(get_completion_report_employee)


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
            newobj =form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Project_Employee_Assign, id=id)
        data = model_to_dict(data)
        data["inspector"] = convent_employee(data["inspector"])
        data["lead_employee"] = convent_employee(data["lead_employee"])
        carry_equipments_ids = [str(equipment.id) for equipment in data["carry_equipments"]]
        data["carry_equipments"] = list(carry_equipments_ids)
        

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
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
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
        data['attachment'] = data['attachment'].url if data['attachment']  else None

        return JsonResponse({"data":data}, status=200,safe = False)



class Quotation_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = QuotationForm(dict_data)
        if form.is_valid():
            if "work_item" in dict_data:
                getQuotation = Quotation.objects.get(id=dict_data['id'])
                get_work_item = [int(item) for item in  dict_data["work_item"]]
                del dict_data["work_item"]
                getQuotation.work_item.set(get_work_item)

                getQuotation.update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)


    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Quotation.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = QuotationForm(request.POST)

        if form.is_valid():
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Quotation, id=id)
        get_id = data.get_show_id()

        work_item_list = []
        for item in data.work_item.all():
            item_dict = model_to_dict(item)
            work_item_list.append(item_dict)

        data = model_to_dict(data)
        print("dict_data")
        print(data)
        data['work_item'] = work_item_list
        data['quotation_id'] = get_id

        return JsonResponse({"data":data}, status=200,safe = False)


class Work_Item_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = Work_ItemForm(dict_data)
        if form.is_valid():
            Work_Item.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)


    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Work_Item.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)


    def post(self,request):
        form = Work_ItemForm(request.POST)

        if form.is_valid():
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Work_Item, id=id)
        data = model_to_dict(data)


        print("dict_data")
        print(data)
        data['work_item_id'] = "WT-" +str(data["id"]).zfill(5)


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




#匯入檔案
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



class Employee_assign_update_signature(View):
   def post(self, request):
        getid = request.POST.get("id")
        uploaded_file = request.POST.get("enterprise_signature")
        print("getid:", getid)
        if(uploaded_file):
            model=Project_Employee_Assign.objects.get(id=getid)

            format, imgstr = uploaded_file.split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            filename = f"signature_{getid}.{ext}"
            model.enterprise_signature.save(filename,data, save=True)
            return JsonResponse({'status': 'success'},status=200)
        else:
            return JsonResponse({"data":"error"}, status=400,safe=False)



class FormUploadFileView(View):
   def post(self, request):
        getname = request.POST.get("name")
        getmodal = request.POST.get("modal")
        getid = request.POST.get("id")
        uploaded_file = request.FILES.get(getname)
        #如果是多對多，就用另一種
        ManyToManyProcess = request.POST.get("ManyToManyProcess",False)
        filename = request.POST.get("file_name","")
        print("getmodel:", getmodal)
        print("getname:", getname)
        print("getid:", getid)
        print("uploaded_file:", uploaded_file)
        print("ManyToManyProcess:", ManyToManyProcess)
        print("filename:", filename)
        
        if(uploaded_file):
            match getmodal:
                case "project_confirmation":
                    model=Project_Confirmation.objects.get(id=getid)
                case "job_assign":
                    model=Project_Job_Assign.objects.get(id=getid)
                case "employee_assign":
                    model=Project_Employee_Assign.objects.get(id=getid)
                case "news":
                    model=News.objects.get(id=getid)
                case "Equipment":
                    model=Equipment.objects.get(id=getid)
                case "employee":
                    model=Employee.objects.get(id=getid)
                case _:
                    return JsonResponse({"data":"no the modal"}, status=400,safe=False)

            if ManyToManyProcess:
                print("xx")
                related_field = getattr(model, getname)
                print("xx")
                uploaded_file_obj = UploadedFile.objects.create(name=filename, file=uploaded_file)
                print("xx")
                related_field.add(uploaded_file_obj)
            else:

                setattr(model, getname, uploaded_file)
                model.save()
            return JsonResponse({'status': 'success'},status=200)
        else:
            return JsonResponse({"data":"error"}, status=400,safe=False)


class Groups_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        group = Group.objects.get(id=dict_data['id'])
        user_ids= dict_data.get("user_set",[])
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
from django.core import serializers

class Approval_Groups_View(View):
    def post(self,request):
        # post 處理兩個事件，【是否勾選直屬主管】以及【送出新關卡(員工)】
        dict_data = convent_dict(request.body)
        print("dict_data ",dict_data)
        approval_target = get_object_or_404(Approval_Target, id=dict_data["set_id"])
        approval_order = approval_target.approval_order

        # 【勾選直屬主管】:
        if dict_data["is_checked"]:
            print("勾選")
            approval_order.insert(0,"x")
            approval_target.approval_order = approval_order
            approval_target.save()
            return JsonResponse({'data': "修改成功"},status=200)
        elif not dict_data["is_checked"]:
        # 【取消勾選直屬主管】:
            print("取消勾選")
            approval_order.remove("x")
            approval_target.approval_order = approval_order
            approval_target.save()
            return JsonResponse({'data': "修改成功"},status=200)
        
        # 【送出新關卡(員工)】:
        employee_id = dict_data["new_stage_id"]
        approval_order.append(employee_id)
        approval_target.approval_order = approval_order
        approval_target.save()
        print("approval_target.approval_order ",approval_target.approval_order)
        
        return JsonResponse({'data': "修改成功"},status=200)

    def get(self, request):
        id = request.GET.get('id')
        data = get_object_or_404(Approval_Target, id=id)
        json_data = model_to_dict(data)
        json_data["is_director"] = False
        approval_order_list = []
        
        for item in json_data['approval_order']:
            if item != "x":
                try:
                    employee = Employee.objects.get(id=item)
                    approval_order_list.append({"id": item, "name": employee.full_name})
                except Employee.DoesNotExist:
                    continue
            elif item == "x":
                json_data["is_director"] = True
        
        json_data["approval_order"]= approval_order_list
        json_data["name"]= data.get_name_display()

        return JsonResponse({"data": json_data}, status=200)
    
    def delete(self, request):
        try:
            dict_data = convent_dict(request.body)
            employee_id = dict_data["new_stage_id"]
            approval_target = get_object_or_404(Approval_Target, id=dict_data["set_id"])
            approval_order = approval_target.approval_order
            approval_order.remove(employee_id)
            approval_target.approval_order = approval_order
            approval_target.save()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)
    
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
                newobj =form.save()
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
            return JsonResponse({'data': "完成修改"},status=200)
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
            username = form.cleaned_data['employee_id']
            password = form.cleaned_data['id_number']
            user = User.objects.create_user(username=username, password=password)
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            return JsonResponse({'data': "完成新增","id":employee.id},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Employee, id=id)
        uploaded_files = data.uploaded_files.all() 
        uploaded_files_dict_list = []
        for file in uploaded_files:
            file_dict = model_to_dict(file)
            file_dict["file"] = file.file.url
            uploaded_files_dict_list.append(file_dict)

        data = model_to_dict(data)
        data["uploaded_files"]=uploaded_files_dict_list
        data['profile_image'] = data['profile_image'].url if data['profile_image']  else None
        print(data)
        return JsonResponse({"data":data}, status=200,safe = False)

# 員工出勤
class Employee_Attendance_View(View):
    def get(self,request):
        department = request.GET.get('department') # 回傳department的id
        full_name = request.GET.get('full_name')
        clock_inout = request.GET.get('clock_inout')
        clock_time_date = request.GET.get('clock_time_date')
        # 篩選部門以及名稱有包含
        employees = Employee.objects.filter(departments__in=[department]).filter(full_name__icontains=full_name)
        # if clock_time_date:
        #     print(clock_time_date)
            # T是簽到F是簽退
            # clock_time_date = employee.clock.filter(created_date__in=[clock_time_date])
        data = []
        for employee in employees:
            print(employee.full_name)
            # 篩選簽到還是簽退以及有無包含過來的日期
            for clock in employee.clock.filter(clock_in_or_out__in=[clock_inout]).filter(created_date__icontains=clock_time_date):
                data.append({
                    'clock_date':clock.created_date,
                    'department': employee.departments.department_name,
                    'employee_id': employee.employee_id,
                    'full_name': employee.full_name,
                    'clock_inout': clock_inout,
                    'clock_out': clock.clock_time,
                    'clock_GPS': clock.clock_GPS,
                })
        

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
            
            get_Quotation_Object = Quotation.objects.get(id=dict_data['quotation'])
            getObject.quotation = get_Quotation_Object
            del dict_data["quotation"]
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
            newobj =form.save()
            return JsonResponse({'data': "完成新增","id":newobj.id},status=200)
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Project_Confirmation, id=id)
        get_id=data.get_show_id()
        project_name=data.quotation.project_name if data.quotation else None
        data = model_to_dict(data)
        data['project_confirmation_id'] = get_id
        data['project_name'] = project_name
        data["completion_report_employee"] = convent_employee(data["completion_report_employee"])
        data['attachment'] = data['attachment'].url if data['attachment']  else None
        print(data)
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
            newobj =form.save()
            return JsonResponse({'data':"完成新增","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Project_Job_Assign, id=id)
        print(data)


        #渲染關聯
        selected_fields = ['id','quotation_id', 'project_name', 'client', 'requisition']
        project_confirmation_dict = model_to_dict(data.project_confirmation, fields=selected_fields)

        data = model_to_dict(data)
        data["lead_employee"] = convent_employee(data["lead_employee"])
        data["work_employee"] = convent_employee(data["work_employee"])
        #將外來鍵的關聯 加入dict
        data['project_confirmation'] = project_confirmation_dict
        data['job_assign_id'] = "工派-" +str(data["id"]).zfill(5)
    
        return JsonResponse({"data":data}, status=200,safe = False)



class ExcelExportView(View):
   def post(self,request):
        json_data = json.loads(request.body)
        headers = json_data['headers']
        table_data = json_data['data']
        # print(table_data) # table_data是[{表頭名:資料內容}]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        
        # 初始化每個欄位的最大長度，以表頭長度為初始值
        max_lengths = [len(header) for header in headers]
        for row_data in table_data:
            # row = [row_data.get(header, '') for header in headers]
            row = [self.replace_br_with_newline(row_data.get(header, '')) for header in headers]
             # 更新每個欄位的最大長度
            max_lengths = [max(max_length, len(str(cell))) for max_length, cell in zip(max_lengths, row)]
            ws.append(row)
        # ws.iter_cols 迭代該列的所有欄，從 1 到 headers 的長度，也就是迭代所有欄位
        for col_idx, col in enumerate(ws.iter_cols(min_col=1, max_col=len(headers))):
            max_length = max(len(str(cell.value)) for cell in col)
            adjusted_width = (max_length + 8)  # 調整列寬的公式
            column_letter = get_column_letter(col_idx + 1)
            ws.column_dimensions[column_letter].width = adjusted_width
        # for col_idx, max_length in enumerate(max_lengths):
        #     adjusted_width = (max_length + 2) * 1.2  # 調整列寬的公式
        #     column_letter = get_column_letter(col_idx + 1)
        #     ws.column_dimensions[column_letter].width = adjusted_width

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=表格数据.xlsx'
        wb.save(response)

        return response
   def replace_br_with_newline(self, data):
        if '<br>' in data:
            return data.replace('<br>', ' ')
        return data

class Calendar_View(View):
   def get(self,request):
        employeeid = request.user.employee
        related_projects = Project_Job_Assign.objects.filter(lead_employee__in=[employeeid])|Project_Job_Assign.objects.filter(work_employee__in=[employeeid])
        data = []
        for project in related_projects:
            if project.attendance_date is None:
                continue
            if project.location is None:
                project.location = "暫無"
            print(project.location)
            data.append({
                'title': project.project_confirmation.project_name,
                'start': project.attendance_date,
                'location': project.location
                # 'start': project.attendance_date.strftime('%Y-%m-%d'),
            })
        return JsonResponse(data, status=200,safe = False)

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



class DeleteUploadedFileView(View):
    def delete(self, request, employee_id, file_id):
        employee = get_object_or_404(Employee, id=employee_id)
        uploaded_file = get_object_or_404(UploadedFile, id=file_id)
        if uploaded_file in employee.uploaded_files.all():
            employee.uploaded_files.remove(uploaded_file)
            employee.save()
            uploaded_file.delete()
            
            return JsonResponse({"message": "檔案已刪除。"}, status=200)
        else:
            return JsonResponse({"message": "檔案不存在或不屬於此員工。"}, status=400)