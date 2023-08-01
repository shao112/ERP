from django import forms
from .models import Project_Job_Assign, Department, Project_Confirmation, Employee,News,Project_Employee_Assign, Vehicle

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

class  GroupForm(BaseModelForm):

    class Meta:
        model = Group
        fields = '__all__'

# 工作派任計畫

class ProjectJobAssignForm(BaseModelForm):

    class Meta:
        model = Project_Job_Assign
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        project_confirmation = cleaned_data.get('project_confirmation')
        attendance_date = cleaned_data.get('attendance_date')
        errors = {}

        if attendance_date !=None:
            for date_str in attendance_date:
                if len(date_str) != 8:
                    errors.setdefault('attendance_date', []).append(
                        f"日期 {date_str} ，請使用yyyymmdd格式(ex:20230707)。"
                    )
                else:
                    year = int(date_str[:4])
                    month = int(date_str[4:6])
                    day = int(date_str[6:8])
                    if not (1 <= month <= 12) or not (1 <= day <= 31):
                        errors.setdefault('attendance_date', []).append(
                            f"日期 {date_str} ，請確認日期數字在合理數字範圍。"
                        )
                    

        if project_confirmation == -1:
            errors.setdefault('project_confirmation', []).append("請選擇有效的工程確認單。")


        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


# 工作派任計畫
class DepartmentForm(BaseModelForm):

    class Meta:
        model = Department
        fields = '__all__'
        
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