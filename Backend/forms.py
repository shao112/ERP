from django.forms import ModelForm
from .models import Project

# 工作派任計畫
class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = '__all__'