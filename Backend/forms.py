from django import forms
from .models import Project, Department, Project_Confirmation

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

# 工程確認單
class ProjectConfirmationForm(BaseModelForm):

    class Meta:
        model = Project_Confirmation
        fields = '__all__'

# 工作派任計畫
class ProjectForm(BaseModelForm):

    class Meta:
        model = Project
        fields = '__all__'

# 工作派任計畫
class DepartmentForm(BaseModelForm):

    class Meta:
        model = Department
        fields = '__all__'

    widgets = {
        'parent_department': forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'id':'parent_department_control'
            }),
        'department_name': forms.TextInput(attrs={'class': 'form-control'}),
        'department_id': forms.TextInput(attrs={'class': 'form-control'})
    }
    labels = {
        'parent_department': '上層部門',
        'department_name': '部門編號',
        'department_id': '部門名稱',
    }