from django import forms
from .models import ExtraWorkDay,Requisition,Client,Travel_Application,Clock_Correction_Application,Leave_Application, Work_Overtime_Application, Leave_Application,Leave_Param,Approval_Target,Quotation,Work_Item,Project_Job_Assign,Department,Equipment,Project_Confirmation,Employee,News,Project_Employee_Assign,Vehicle,ApprovalModel

from django.contrib.auth.models import Group

from ERP.settings import DEBUG

#base modelform
class BaseModelForm(forms.ModelForm):
    def get_chinese_field_name(self, field_name):
        field = self.fields.get(field_name)
        if field:
            return field.label or field_name
        return field_name

    def get_error_messages(self):
        #根據debug，來顯示要不要顯示對應的欄位英文
        
        error_messages = []
        for field, errors in self.errors.items():
            chinese_field_name = self.get_chinese_field_name(field)
            if DEBUG:
                error_messages.append(f"{chinese_field_name}({field}): {', '.join(errors)}")
            else:
                error_messages.append(f"{chinese_field_name}: {', '.join(errors)}")
        return '\n'.join(error_messages)

    def is_valid(self):
        valid = super().is_valid()
        if 'created_date' in self.errors:
            del self.errors['created_date']
        # print(valid)

        return  not bool(self.errors)

class SalaryEmployeeForm(BaseModelForm):
    class Meta:
        model = Employee
        fields = ['default_salary', 'job_addition', 'phone_addition',  'certificates_addition', 'labor_protection', 'health_insurance', 'labor_pension']
        widgets = {
            'default_salary': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'default_salary', 'required': 'required', 'value': '0'}),
            'job_addition': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'job_addition', 'required': 'required', 'value': '0'}),
            'phone_addition': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'phone_addition', 'required': 'required', 'value': '0'}),
            'certificates_addition': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'certificates_addition', 'required': 'required', 'value': '0'}),
            'labor_protection': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'labor_protection', 'required': 'required', 'value': '0'}),
            'health_insurance': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'health_insurance', 'required': 'required', 'value': '0'}),
            'labor_pension': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'name': 'labor_pension', 'required': 'required', 'value': '0'}),
        }

        

# 最新公告表單
class NewsForm(BaseModelForm):

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'level': forms.Select(attrs={'class': 'form-control form-control-sm'})
        }


class QuotationForm(BaseModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

class Travel_ApplicationForm(BaseModelForm):
    class Meta:
        model = Travel_Application
        fields = '__all__'
        widgets = {
            'location_city_go': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'location_city_go', "name":'location_city_go', 'required': 'true'}),
            'location_city_end': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'location_city_end', "name":'location_city_end', 'required': 'true'}),
            }

class ExtraWorkDayForm(BaseModelForm):
    class Meta:
        model = ExtraWorkDay
        fields = '__all__'
        

class Work_ItemForm(BaseModelForm):
    class Meta:
        model = Work_Item
        fields = '__all__'
        
class ClientForm(BaseModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        client_name = cleaned_data.get('client_name')
        errors = {}

        if not client_name:
            errors['client_name'] = "請輸入請購單為名稱"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

class RequisitionForm(BaseModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        requisition_name = cleaned_data.get('requisition_name')
        errors = {}

        if not requisition_name:
            errors['requisition_name'] = "請輸入請購單為名稱"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

# 資產確認單
class EquipmentForm(BaseModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'

# 工程確認單
class ProjectConfirmationForm(BaseModelForm):

    class Meta:
        model = Project_Confirmation
        fields = '__all__'
        widgets = {
            'requisition': forms.Select(attrs={'class': 'form-control form-control-sm readonly', 'id':'requisition', 'name':'requisition'}),
        }


# 派工單
class Project_Employee_AssignForm(BaseModelForm):

    class Meta:
        model = Project_Employee_Assign
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        construction_date = cleaned_data.get('construction_date')
        errors={}
        if  construction_date =="":
            errors['construction_date'] = "請選擇施工日期"
        if errors:
            raise forms.ValidationError(errors)


# 工作派任計畫
class ProjectJobAssignForm(BaseModelForm):

    class Meta:
        model = Project_Job_Assign
        fields = '__all__'
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'location', 'name':'location',"required":"true"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        # 工作派任計畫必填欄位：工程確認單、出勤日期、工作方式(是:出勤、否:文書)、工作人員、工作地點
        project_confirmation = cleaned_data.get('project_confirmation')
        attendance_date = cleaned_data.get('attendance_date')
        work_method = cleaned_data.get('work_method',"")
        print(work_method)
        work_employee = cleaned_data.get('work_employee')
        location = cleaned_data.get('location')
        construction_date = cleaned_data.get('construction_date')
        errors = {}


        if project_confirmation == -1:
            # errors.setdefault('project_confirmation', []).append("請選擇有效的工程確認單。") # 原本寫法
            errors['project_confirmation'] = "請選擇有效的工程確認單。"
        if not attendance_date:
            errors['attendance_date'] = "請選擇出勤日期。"

        if  work_method =="":
            errors['work_method'] = "請選擇工作方法。"


        if not location:
            errors['location'] = "請選擇工作地點。"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


# 部門
class DepartmentForm(BaseModelForm):
    def clean(self):
        cleaned_data = super().clean()
#            raise forms.ValidationError("上層部門不能與自己相同。")
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'belong_to_company': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'belong_to_company_control'}),
        }
        
# 員工
class EmployeeForm(BaseModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'location_city': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'location_city', "name":'location_city', 'required': 'true'}),
            'departments': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'departments', "name":'departments', 'required': 'true'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'gender', "name":'gender', 'required': 'true'}),
            'blood_type': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'blood_type', "name":'blood_type'}),
            'marital_status': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'marital_status', "name":'marital_status'}),
            'military_status': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'military_status', "name":'military_status'})
        }
        def clean(self):
            cleaned_data = super().clean()
            # 員工必填欄位：員工名稱、員工ID、部門名稱、身份證字號、職稱、居住城市(用於計算)
            full_name = cleaned_data.get('full_name')
            employee_id = cleaned_data.get('employee_id')
            departments = cleaned_data.get('departments')
            id_number = cleaned_data.get('id_number')
            position = cleaned_data.get('position')
            location_city = cleaned_data.get('location_city')
            errors = {}
            
            if not full_name:
                errors['full_name'] = "請輸入員工名稱。"

            if not employee_id:
                errors['employee_id'] = "請輸入員工ID"

            if not departments:
                errors['departments'] = "請輸入部門名稱"

            if not id_number:
                errors['id_number'] = "請輸入身份證字號"

            if not position:
                errors['position'] = "請輸入職稱"

            if not location_city:
                errors['location_city'] = "請輸入居住城市"


            if errors:
                raise forms.ValidationError(errors)

            return cleaned_data
# 員工
class VehicleForm(BaseModelForm):

    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
# 簽核狀態
class ApprovalModelForm(BaseModelForm):

    class Meta:
        model = ApprovalModel
        fields = '__all__'
        widgets = {
            'current_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

# 請假參數
class LeaveParamModelForm(BaseModelForm):

    class Meta:
        model = Leave_Param
        fields = '__all__'
        def clean(self):
            cleaned_data = super().clean()
            start_hours_of_leave = cleaned_data.get('start_hours_of_leave')
            errors = {}
            
            if start_hours_of_leave <=5:
                errors['start_hours_of_leave'] = "起始時間請至少6點。"


            if errors:
                raise forms.ValidationError(errors)

            return cleaned_data

# 請假申請
class LeaveApplicationForm(BaseModelForm):

    class Meta:
        model = Leave_Application
        fields = '__all__'
        widgets = {
            'type_of_leave': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'type_of_leave', 'name':'type_of_leave','required': True}),
            'substitute': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'substitute', 'name':'substitute','required': True}),
        }
        def clean(self):
            cleaned_data = super().clean()
            substitute = cleaned_data.get('substitute')
            errors = {}
            
            if not substitute:
                errors['substitute'] = "請選擇代理人。"
            if errors:
                raise forms.ValidationError(errors)

            return cleaned_data

# 加班申請
class WorkOvertimeApplicationForm(BaseModelForm):

    class Meta:
        model = Work_Overtime_Application
        fields = '__all__'
        widgets = {
            'shift_of_overtime': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'shift_of_overtime', 'name':'shift_of_overtime'}),
            'type_of_overtime': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'type_of_overtime', "name":'type_of_overtime'}),
            'carry_over': forms.Select(attrs={'class': 'form-control form-control-sm', 'id':'carry_over', "name":'carry_over'}),
        }
# 補卡申請
class ClockCorrectionApplicationForm(BaseModelForm):

    class Meta:
        model = Clock_Correction_Application
        fields = '__all__'
        widgets = {
            'shift_of_clock': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'category_of_clock': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'type_of_clock': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
