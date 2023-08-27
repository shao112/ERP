from django import forms
from .models import Approval_TargetDepartment, Quotation,Work_Item,Project_Job_Assign, Department, Equipment,Project_Confirmation, Employee,News,Project_Employee_Assign, Vehicle,ApprovalModel

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
        

class Work_ItemForm(BaseModelForm):
    class Meta:
        model = Work_Item
        fields = '__all__'
        



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

# 派工單
class Project_Employee_AssignForm(BaseModelForm):

    class Meta:
        model = Project_Employee_Assign
        fields = '__all__'




# 工作派任計畫

class ProjectJobAssignForm(BaseModelForm):

    class Meta:
        model = Project_Job_Assign
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        project_confirmation = cleaned_data.get('project_confirmation')
        errors = {}


        if project_confirmation == -1:
            errors.setdefault('project_confirmation', []).append("請選擇有效的工程確認單。")

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
            'gender': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'blood_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'marital_status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'military_status': forms.Select(attrs={'class': 'form-control form-control-sm'})
        }
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

