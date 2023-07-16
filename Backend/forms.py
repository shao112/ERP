from django import forms
from .models import Project_Job_Assign, Department, Project_Confirmation, Employee

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

# 工程確認單
class ProjectConfirmationForm(BaseModelForm):

    class Meta:
        model = Project_Confirmation
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