from django import forms
from .models import Project, Department

# 工作派任計畫
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'

# 工作派任計畫
class DepartmentForm(forms.ModelForm):

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