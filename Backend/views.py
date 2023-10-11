from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed,HttpResponseRedirect,HttpResponse,Http404
import json,datetime
from django.contrib.auth import update_session_auth_hash
import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from Backend.models import  Travel_Application, ExtraWorkDay,Requisition,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail, Client,Leave_Application,Leave_Param,SysMessage,Approval_Target, Equipment, UploadedFile,Department,Quotation,ApprovalLog,Work_Item,ApprovalModel, Project_Confirmation, Employee, Project_Job_Assign,News,Clock,Project_Employee_Assign
from Backend.forms import Travel_ApplicationForm,ExtraWorkDayForm,RequisitionForm, ClientForm, ClockCorrectionApplicationForm, WorkOvertimeApplicationForm, LeaveParamModelForm,LeaveApplicationForm,ProjectConfirmationForm,EquipmentForm,QuotationForm,DepartmentForm,Work_ItemForm,  EmployeeForm, ProjectJobAssignForm,NewsForm,Project_Employee_AssignForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import PasswordChangeForm
from urllib.parse import parse_qs
from urllib.parse import quote
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from .utils import quotationFile,convent_dict,convent_employee,salaryFile,convent_excel_dict,match_excel_content,get_model_by_name
from .salary_utils import create_salary
import openpyxl
from openpyxl import load_workbook

from openpyxl.utils import get_column_letter
from django.db.utils import IntegrityError
import random,os,re
from  django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from datetime import time

from django.utils.text import get_valid_filename # 確保file檔名是合法的，不接受的符號會轉成可接受符號


import zipfile


class QuotationFileView(View):

    def get(self, request, *args, **kwargs):
        obj_id = self.kwargs.get('id')
        see = self.kwargs.get('see')
        five = self.kwargs.get('five')
        
        if id:
            error_msg=""
            try:
                quotaion_obj = Quotation.objects.get(id=obj_id)
                print("quotaion_obj ",quotaion_obj)
            except Http404:
                return JsonResponse({"error": "找不到相應的ID obj"}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({"error": str(e)}, status=400)
            
            return quotationFile(quotaion_obj,see,five)

        else:
            print("error 找不到相應的ID obj")
            return JsonResponse({"error": "找不到相應的ID obj"}, status=400)
       
        
class SalaryFileView(View):

    def get(self, request, *args, **kwargs):
        year, month, user = self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('user')
        use_type =  self.kwargs.get('use_type')
        use_type = bool(int(use_type))
        title=""
        if use_type:
            title = "薪資條"
        else:
            title = "激勵性獎金"
        
        if user==0:#全員
            getEm = Employee.objects.all()
            error_msg=""
            file_paths=[]
            for employee in getEm:
                try:
                    get_salary = Salary.objects.get(user=employee, year=year, month=month)
                except Http404:
                    error_msg +=f"找不到{employee.full_name}的當月薪資單 \n"
                    continue
                except Exception as e:
                    error_msg +=f"找不到{employee.full_name} 其他錯誤，如沒有部門 \n"
                    continue
                       
                error,obj = salaryFile(get_salary,use_type)

                if error:
                    error_msg += f"{obj} \n"
                else:      
                    file_paths.append({"file_name":obj,"name":f"{year}_{month}_{title}/{employee.full_name}_{year}_{month}_{title}.xlsx"})
                
            filename = f'media/salary_files/全員_{year}_{month}_{title}.zip'
            quoted_filename = quote(filename)

            with zipfile.ZipFile(filename, 'w') as archive:
                for file_info in file_paths:
                    file_name = file_info["file_name"]
                    name = file_info["name"]
                    archive.write(file_name, arcname=name)

            with open(filename, 'rb') as file:
                response = HttpResponse(file, content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{quoted_filename}"'
                response['Content-Length'] = os.path.getsize(filename)

            print(error_msg)
            return response

        else:
            try:
                get_salary = Salary.objects.get(user=user, year=year, month=month)
            except Http404:
                return JsonResponse({"error": "找不到相應的ID obj"}, status=400)
       
            error,obj = salaryFile(get_salary,use_type)

            if error:
                return JsonResponse({"error":obj},status=400)
         

            with open(obj, 'rb') as file:
                filename = f"{get_salary.user.full_name}_{year}_{month}_{title}.xlsx"
                print(filename)
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={quote(filename)}'

            return response



class SalaryDetailView(View):
    def delete(self, request, *args, **kwargs):
        dict_data = convent_dict(request.body)

        id = int(dict_data.get('itemid'))
        try:
            get_obj = get_object_or_404(SalaryDetail, id=id)
        except Http404:
            return JsonResponse({"error": "找不到相應的明細 obj"}, status=400)
        get_obj.delete()
        return JsonResponse({"ok":"ok"},status=200)

    def put(self, request, *args, **kwargs):
        dict_data = convent_dict(request.body)

        id = int(dict_data.get('itemid'))
        name = dict_data.get('name') 
        deduction = dict_data.get('deduction')
        tax_deduction = dict_data.get('tax_deduction')
        five = dict_data.get('five')
        adjustmentAmount = int(dict_data.get('adjustmentAmount'))

        if adjustmentAmount <0:
            return JsonResponse({"error": "調整金額需大於0，如需扣款請勾選為扣款項"}, status=400)

        try:
            get_obj = get_object_or_404(SalaryDetail, id=id)
        except Http404:
            return JsonResponse({"error": "找不到相應的ID obj"}, status=400)

        get_obj.set_name_and_adjustment_amount(name, adjustmentAmount,deduction,tax_deduction=tax_deduction,five=five)  

        return JsonResponse({"ok":"ok"},status=200)

    def post(self, request, *args, **kwargs):
        dict_data = convent_dict(request.body)
        moneyValue = dict_data.get('moneyValue',0)
        if int(moneyValue) <= 0:
            return JsonResponse({"error": "金額需大於0"}, status=400)

        name = dict_data.get('name')
        deductionValue = dict_data.get('deduction')
        tax_deduction = dict_data.get('tax_deduction')
        five = dict_data.get('five')
        year, month, user = self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('user')
        try:
            get_salary =Salary.objects.get(user=user, year=year, month=month)
        except Http404:
            return JsonResponse({"error": "找不到相應的ID obj"}, status=400)

        SalaryDetail.objects.create(
            salary=get_salary,
            name=name,
            system_amount=moneyValue,  
            adjustment_amount=moneyValue,
            deduction=deductionValue,
            tax_deduction=tax_deduction,
            five=five,
        )
        return JsonResponse({"ok":"ok"},status=200)


        

class SalaryListView(View):
    def post(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        user_id = kwargs.get('user_id')
        print(year, month,user_id)
        if user_id:
            employee = Employee.objects.get(id=user_id)
            create_salary(employee, year, month)
        else:
            employees = Employee.objects.all()
            for employee in employees:
                create_salary(employee, year, month)
           

        return JsonResponse({"ok":"ok"},status=200)
        # return JsonResponse({"error":"找不到model"},status=400)


class SysMessage_API(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        id = data.get('id')  
        getobj = SysMessage.objects.get(id=id)
        getobj.delete() 
        return HttpResponse(200)

class Approval_View_Process(View):
    def post(self,request):
        new_Approval=None
        
        try:
            id = request.POST.get('id')
            modeltext = request.POST.get('model')

            getmodel = get_model_by_name(modeltext)
            if getmodel is  None:
                return JsonResponse({"error":"找不到model"},status=400)

            try:
                get_obj = get_object_or_404(getmodel, id=id)
            except Http404:
                return JsonResponse({"error": "找不到相應的ID obj"}, status=400)
            
            model_name = {# 對應Approval_Target的name
                'project_confirmation': 'Project_Confirmation',
                'job_assign': 'Project_Job_Assign',
                'Project_Employee_Assign': 'Project_Employee_Assign',
                'Work_Overtime_Application': 'Work_Overtime_Application',
                'Leave_Application': 'Leave_Application',
                'Clock_Correction_Application': 'Clock_Correction_Application',
                'Travel_Application': 'Travel_Application',
            }
            print("modeltext: ", modeltext)

            try:
                get_Approval_Target = get_object_or_404(Approval_Target, name=model_name.get(modeltext))
            except Http404:
                return JsonResponse({"error": "找不到相應的簽核目標"}, status=400)
            
            get_order = get_Approval_Target.approval_order

            if modeltext =="Leave_Application": #請假單
                get_user = get_obj.substitute
                if get_user :
                    get_user_id= get_user.id
                    get_order.insert(0, get_user_id ) #先給代理人簽核
                else:
                    return JsonResponse({"error": "請選擇代理人"}, status=400)



            new_Approval= ApprovalModel.objects.create(target_approval=get_Approval_Target,order=get_order)
            if get_obj.Approval !=None:
                get_obj.Approval.delete()
            get_obj.Approval=new_Approval
            get_obj.save()

            employee_id = new_Approval.target_approval.approval_order[0]
            if  employee_id !="x":
                sender = Employee.objects.get(id=employee_id)
                SysMessage.objects.create(Target_user=sender,content=f"您有一筆 {new_Approval.target_approval.get_name_display()} 單需要簽核")
            else:
                print("new_Approval")
                print(new_Approval.get_created_by)

                senders = new_Approval.get_created_by.departments.employees.filter(user__groups__name='主管')
                for sender in senders:
                    SysMessage.objects.create(Target_user=sender,content=f"您有一筆 {new_Approval.target_approval.get_name_display()} 單需要簽核")


            return JsonResponse({"success":"成功"},status=200)
        except Exception as e:
            if new_Approval !=None: #刪除出錯的簽核執行obj
                new_Approval.delete()
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
            return JsonResponse({"error": "找不到相應的ID obj"}, status=400)
        
        user = request.user.employee
        approval_obj = get_obj.Approval

        if approval_obj.current_status == 'in_process':
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
            return JsonResponse({"error": "找不到相應的ApprovalModel"}, status=400)

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

            if "test_items" in dict_data:
                get_Project_Employee_Assign.test_items = ','.join(map(str, dict_data["test_items"]))
                del dict_data["test_items"]
            else:
                get_Project_Employee_Assign.test_items = ""

            if "carry_equipments" in dict_data:
                get_carry_equipments = dict_data["carry_equipments"]
                get_carry_equipments = [int(item) for item in get_carry_equipments]
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
        print(request.POST)
        get_test_items = request.POST.getlist("test_items")
        form = Project_Employee_AssignForm(request.POST)

        if form.is_valid():
            newobj =form.save()
            newobj.test_items = ','.join(map(str, get_test_items))
            newobj.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)


    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Project_Employee_Assign, id=id)
        get_id=data.get_show_id()
        location = data.project_job_assign.location
        data = model_to_dict(data)
        data["inspector"] = convent_employee(data["inspector"])
        data["lead_employee"] = convent_employee(data["lead_employee"])
        carry_equipments_ids = [str(equipment.id) for equipment in data["carry_equipments"]]
        data["carry_equipments"] = list(carry_equipments_ids)
        data["show_id"] = get_id
        data["location"] = location
        
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
            
            if "client" in dict_data:
                get_obj = Client.objects.get(pk=int(dict_data["client"]))
                getQuotation.client = get_obj
                del dict_data["client"]

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

        uploaded_files = data.uploaded_files.all() 
        uploaded_files_dict_list = []
        for file in uploaded_files:
            file_dict = model_to_dict(file)
            file_dict["file"] = file.file.url
            uploaded_files_dict_list.append(file_dict)
            

        work_item_list = []
        for item in data.work_item.all():
            item_dict = model_to_dict(item)
            work_item_list.append(item_dict)
        client_name=data.client.client_name if data.client else None
        data = model_to_dict(data)
        print("dict_data")
        print(data)
        data["uploaded_files"]=uploaded_files_dict_list
        data['work_item'] = work_item_list
        data['quotation_id'] = get_id
        data['client_name'] = client_name


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

class Client_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = ClientForm(dict_data)
        if form.is_valid():
            Client.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Client.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = ClientForm(request.POST)
        if form.is_valid():
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Client, id=id)
        data = model_to_dict(data)
        return JsonResponse({"data":data}, status=200,safe = False)
    
class ExtraWorkDay_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = ExtraWorkDayForm(dict_data)
        if form.is_valid():
            ExtraWorkDay.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            ExtraWorkDay.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = ExtraWorkDayForm(request.POST)
        if form.is_valid():
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(ExtraWorkDay, id=id)
        data = model_to_dict(data)
        return JsonResponse({"data":data}, status=200,safe = False)
    
class Requisition_View(View):
    def put(self,request):
        dict_data = convent_dict(request.body)
        form = RequisitionForm(dict_data)
        if form.is_valid():
            Requisition.objects.get(id=dict_data['id']).update_fields_and_save(**dict_data)
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Requisition.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = RequisitionForm(request.POST)
        if form.is_valid():
            newobj = form.save()
            return JsonResponse({"data":"新增成功","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Requisition, id=id)
        data = model_to_dict(data)
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
             return JsonResponse({'error': '請上傳檔案'}, status=400)
        #檢查type，回傳上傳正確檔案

        workbook = load_workbook(uploaded_file)
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
                case "Quotation":
                    model=Quotation.objects.get(id=getid)
                case "Leave_Application":
                    model=Leave_Application.objects.get(id=getid)
                case "travel_application":
                    model=Travel_Application.objects.get(id=getid)
                case "Work_Overtime_Application":
                    model=Work_Overtime_Application.objects.get(id=getid)
                case "Clock_Correction_Application":
                    model=Clock_Correction_Application.objects.get(id=getid)
                case _:
                    return JsonResponse({"data":"no the modal"}, status=400,safe=False)

            if ManyToManyProcess:
                related_field = getattr(model, getname)
                uploaded_file_obj = UploadedFile.objects.create(name=filename, file=uploaded_file)
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

class Approval_Groups_View(View):
    def post(self,request):
        # post 處理兩個事件，【是否勾選直屬主管】以及【送出新關卡(員工)】
        dict_data = convent_dict(request.body)
        print("dict_data ",dict_data)
        approval_target = get_object_or_404(Approval_Target, id=dict_data["set_id"])
        approval_order = approval_target.approval_order

        
        if "is_checked" in dict_data:
            # 【勾選直屬主管】:
            if dict_data["is_checked"]:
                print("勾選")
                approval_order.insert(0,"x")
                approval_target.approval_order = approval_order
                approval_target.save()
                return JsonResponse({'data': "修改成功"},status=200)
            else:
            # 【取消勾選直屬主管】:
                print("取消勾選")
                while "x" in approval_order:
                    approval_order.remove("x")
                approval_target.approval_order = approval_order
                approval_target.save()
                return JsonResponse({'data': "修改成功"},status=200)
        
        # 【送出新關卡(員工)】:
        employee_id = int(dict_data["new_stage_id"])
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
            employee_id = int(dict_data["employee_id"])

            approval_target = get_object_or_404(Approval_Target, id=dict_data["set_id"])
            approval_order = approval_target.approval_order
            print("del: ",employee_id)
            print("Befor    : ",approval_order)
            approval_order = [x for x in approval_order if x != employee_id]
            print("after: ",approval_order)
            approval_target.approval_order = approval_order
            approval_target.save()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)

class Leave_Application_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = LeaveApplicationForm(dict_data)
        if form.is_valid():
            getObject = Leave_Application.objects.get(id=dict_data['id'])
            if "type_of_leave" in dict_data:
                type_of_leave = dict_data["type_of_leave"]
                del dict_data["type_of_leave"]
                getObject.type_of_leave = Leave_Param.objects.get(id=type_of_leave)
            if "substitute" in dict_data:
                substitute = dict_data["substitute"]
                del dict_data["substitute"]
                getObject.substitute = Employee.objects.get(id=substitute)
            
            getObject.update_fields_and_save(**dict_data)
            return JsonResponse({'data': "完成修改"},status=200)
        else:
            return JsonResponse({"error":form.errors},status=400)


    def post(self,request):
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            get_leave_id = form.cleaned_data["type_of_leave"].id
            newobj =form.save(commit=False)
            leave_obj =Leave_Param.objects.get(id=get_leave_id)

             
            can_leave = leave_obj.exceeds_leave_quantity_by_year(newobj,request.user.employee)
            
            print("xccc")
            
            if can_leave:
                newobj.save()
                return JsonResponse({'data': "完成新增","id":newobj.id},status=200)
            else:
                return JsonResponse({"error":"無法請假，已沒有請假時數"},status=400)
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    
    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Leave_Application, id=id)
        data = model_to_dict(data)
        data['attachment'] = data['attachment'].url if data['attachment']  else None
        return JsonResponse({"data":data}, status=200,safe = False)
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Leave_Application.objects.get(id=int(dict_data['id'])).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)

class Clock_Correction_Application_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = ClockCorrectionApplicationForm(dict_data)
        if form.is_valid():
            getObject = Clock_Correction_Application.objects.get(id=dict_data['id'])
            if(getObject.Approval ):
                if(getObject.Approval.current_status=="completed" or getObject.Approval.current_status=="in_process" ):            
                    return JsonResponse({"error":"簽核進行或完成禁止修改"},status=400)

            employee = Employee.objects.get(id=request.user.employee.id)
            getObject.update_fields_and_save(**dict_data)
            clock_time = time(int(getObject.end_hours_of_clock), int(getObject.end_mins_of_clock))

            getObject.create_and_update_clock(employee, getObject.date_of_clock, getObject.type_of_clock, clock_time)
            return JsonResponse({'data': "完成修改"},status=200)
        else:
            return JsonResponse({"error":form.errors},status=400)


    def post(self,request):
        form = ClockCorrectionApplicationForm(request.POST)
        if form.is_valid():
            newobj = form.save()
            employee = Employee.objects.get(id=request.user.employee.id)
            clock_time = time(newobj.end_hours_of_clock, newobj.end_mins_of_clock)
            newobj.create_and_update_clock(employee, newobj.date_of_clock, newobj.type_of_clock, clock_time)
            return JsonResponse({'data': "完成新增","id":newobj.id},status=200)
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    
    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Clock_Correction_Application, id=id)
        data = model_to_dict(data)
        data['attachment'] = data['attachment'].url if data['attachment']  else None
        return JsonResponse({"data":data}, status=200,safe = False)
    
    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Clock_Correction_Application.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)

class Work_Overtime_Application_View(View):

    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Work_Overtime_Application.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)


    def put(self,request):
        dict_data = convent_dict(request.body) 
        form = WorkOvertimeApplicationForm(dict_data)
        if form.is_valid():
            getObject = Work_Overtime_Application.objects.get(id=dict_data['id'])
            getObject.update_fields_and_save(**dict_data)
            return JsonResponse({'data': "完成修改"},status=200)
        else:
            return JsonResponse({"error":form.errors},status=400)


    def post(self,request):
        form = WorkOvertimeApplicationForm(request.POST)
        if form.is_valid():
            newobj = form.save()
            return JsonResponse({'data': "完成新增","id":newobj.id},status=200)
        else:
            print("is_valid FALSE")
            error_messages = form.get_error_messages()
            print(error_messages)
            return JsonResponse({"error":error_messages},status=400)

    
    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Work_Overtime_Application, id=id)
        data = model_to_dict(data)
        data['attachment'] = data['attachment'].url if data['attachment']  else None
        return JsonResponse({"data":data}, status=200,safe = False)


class Leave_Param_View(View):
    def post(self,request):
        id = request.POST.get("id")
        form = LeaveParamModelForm(request.POST)

        if form.is_valid():
            is_audit = request.POST.get('is_audit') == 'true'
            is_attachment = request.POST.get('is_attachment') == 'true'
            data = {
                'leave_name': request.POST['leave_name'],
                'leave_quantity': request.POST['leave_quantity'],
                'minimum_leave_number': request.POST['minimum_leave_number'],
                'minimum_leave_unit': request.POST['minimum_leave_unit'],
                'is_audit': is_audit,
                'is_attachment': is_attachment,
                'deduct_percentage': request.POST['deduct_percentage']
            }
            getobj = Leave_Param.objects.get(id=id)
            getobj.update_fields_and_save(**data)    
            return JsonResponse({'data': "修改成功"},status=200)
        else:
            error_messages = form.get_error_messages()
            return JsonResponse({"error":error_messages},status=400)



class Profile_View(View):
    # 同一個post要處理更新照片以及更新密碼
    def post(self,request):
        print("Profile_View")
        if 'profile_image' in request.FILES:
            uploaded_image = request.FILES.get('profile_image')
            employee = get_object_or_404(Employee, id=request.user.employee.id)
            print(employee.profile_image.path)
            print(employee)
            now = datetime.datetime.now()
            date_time_string = now.strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(uploaded_image.name)[1]
            new_file_name = f"{date_time_string}{file_extension}"
            employee.profile_image.save(new_file_name, uploaded_image)
            print("成功")
            return JsonResponse({'status': 'success'},status=200)
        else:
            print("xx")
            print(request.POST)
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
            if "labor_pension" in dict_data:
                if int(dict_data['labor_pension']) <6:
                    return JsonResponse({"error":"勞退比例至少要為6%"},status=400)


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
        data["annualleaves"] = ""
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
                    'clock_date':clock.clock_date,
                    'department': employee.departments.department_name,
                    'employee_id': employee.employee_id,
                    'full_name': employee.full_name,
                    'clock_inout': clock_inout,
                    'clock_out': clock.clock_time,
                    'clock_GPS': clock.clock_GPS,
                })
        

        return JsonResponse({"data":data}, status=200,safe = False)



class Project_Confirmation_View(UserPassesTestMixin,View):
    def test_func(self):
        op = self.request.user.groups.filter(name__icontains='工程確認單管理').exists() #最高權限
        if op  or settings.PASS_TEST_FUNC:
            return True
        if self.request.method == 'GET':
            return self.request.user.groups.filter(name__icontains='工程確認單查看').exists()


    def put(self,request):
        dict_data = convent_dict(request.body)
        form = ProjectConfirmationForm(dict_data)
        if form.is_valid():
            getObject = Project_Confirmation.objects.get(id=dict_data['id'])
            if "completion_report_employee" in dict_data:
                get_completion_report_employee = dict_data["completion_report_employee"]
                del dict_data["completion_report_employee"]
                getObject.completion_report_employee.set(get_completion_report_employee)

            if "requisition" in dict_data:
                get_requisition_id = dict_data["requisition"]
                del dict_data["requisition"]
                getObject.requisition = Requisition.objects.get(id=get_requisition_id)
            
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
        requisition_name=data.requisition.requisition_name if data.requisition else None
        client_name=data.quotation.client.client_name if data.quotation.client else None

        data = model_to_dict(data)
        data['requisition_name'] = requisition_name
        data['project_confirmation_id'] = get_id
        data['project_name'] = project_name
        data['client_name'] = client_name
        data["completion_report_employee"] = convent_employee(data["completion_report_employee"])
        data['attachment'] = data['attachment'].url if data['attachment']  else None
        print(data)
        return JsonResponse({"data":data}, status=200,safe = False)

class Job_Assign_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = ProjectJobAssignForm(dict_data)
        if form.is_valid():
            getObject = Project_Job_Assign.objects.get(id=int(dict_data['id']))
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
            print("error_messages: ",error_messages)
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Project_Job_Assign, id=id)
        show_data_id= data.get_show_id()
        #渲染關聯
        selected_fields = ['id','quotation_id', 'quotation', 'client', 'requisition']
        quotation_selected_fields = ['id','project_name',  'client']
        requisition_name = ""
        if data.project_confirmation.requisition:
            requisition_name =data.project_confirmation.requisition.requisition_name
        project_confirmation_dict = model_to_dict(data.project_confirmation, fields=selected_fields)
        
        quotation_dict = model_to_dict(data.project_confirmation.quotation,fields=quotation_selected_fields)
        q_id= data.project_confirmation.quotation.get_show_id()
        client_name= data.project_confirmation.quotation.client.client_name
        quotation_dict["q_id"] = q_id
        quotation_dict["client_name"] = client_name

        data = model_to_dict(data)
        data["requisition_name"]=requisition_name
        data["lead_employee"] = convent_employee(data["lead_employee"])
        data["work_employee"] = convent_employee(data["work_employee"])
        #將外來鍵的關聯 加入dict
        data['project_confirmation'] = project_confirmation_dict
        data['quotation_dict'] = quotation_dict
        data['job_assign_id'] = show_data_id
        return JsonResponse({"data":data}, status=200,safe = False)


class Travel_Application_View(View):

    def put(self,request):
        dict_data = convent_dict(request.body)
        form = Travel_ApplicationForm(dict_data)
        if form.is_valid():
            getObject = Travel_Application.objects.get(id=int(dict_data['id']))
            getObject.update_fields_and_save(**dict_data)

            return JsonResponse({'data': "完成修改"},status=200)
        else:
            return JsonResponse({"error":form.errors},status=400)


    def delete(self,request):
        try:
            dict_data = convent_dict(request.body)
            Travel_Application.objects.get(id=dict_data['id']).delete()
            return HttpResponse("成功刪除",status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"資料不存在"},status=400)
        except  Exception as e:
            print(e)
            return JsonResponse({"error":str(e)},status=500)

    def post(self,request):
        form = Travel_ApplicationForm(request.POST)

        if form.is_valid():
            newobj =form.save()
            return JsonResponse({'data':"完成新增","id":newobj.id},status=200)
        else:
            error_messages = form.get_error_messages()
            print("error_messages: ",error_messages)
            return JsonResponse({"error":error_messages},status=400)

    def get(self,request):
        id = request.GET.get('id')
        data = get_object_or_404(Travel_Application, id=id)
        show_data_id= data.get_show_id()
        data = model_to_dict(data)
        data["show_data_id"]=show_data_id
        data['attachment'] = data['attachment'].url if data['attachment']  else None

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
            data.append({
                'title': project.project_confirmation.quotation.project_name,
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
    def delete(self, request,model, obj_id, file_id):
        match model:
            case "employee":
                model=Employee.objects.get(id=obj_id)
            case "Quotation":
                model=Quotation.objects.get(id=obj_id)

        uploaded_file = get_object_or_404(UploadedFile, id=file_id)
        if uploaded_file in model.uploaded_files.all():
            model.uploaded_files.remove(uploaded_file)
            model.save()
            uploaded_file.delete()            
            return JsonResponse({"message": "檔案已刪除。"}, status=200)
        else:
            return JsonResponse({"message": "檔案不存在或不屬於此員工。"}, status=400)