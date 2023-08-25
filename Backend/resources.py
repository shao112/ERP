from import_export import resources, fields,widgets
from import_export.fields import Field

from django.conf import settings # 要取得 BASE_URL

from .models import Department, Project_Confirmation, Project_Job_Assign, Project_Employee_Assign

# 匯出布林值欄位只會顯示 1 跟 0，要特別處理布林值
class BooleanWidget(widgets.BooleanWidget):
    def render(self, value, obj):
        if value in self.NULL_VALUES:
            return ""
        return '是' if value else '否'

# 工程確認單編號匯出要變成 工確+id
class ConfirmationIDWidget(widgets.Widget):
    def render(self, value, obj=None):
        format_value = f"工確-{value:05d}".format(value=value)
        return format_value
# 工作派任計畫編號匯出要變成 派任+id
class JobAssignIDWidget(widgets.Widget):
    def render(self, value, obj=None):
        format_value = f"派任-{value:05d}".format(value=value)
        return format_value
# 派工單編號匯出要變成 派工+id
class EmployeeAssignIDWidget(widgets.Widget):
    def render(self, value, obj=None):
        format_value = f"派工-{value:05d}".format(value=value)
        return format_value

class DepartmentResource(resources.ModelResource):
    belong_to_company = Field(attribute='belong_to_company', column_name=Department.belong_to_company.field.verbose_name)
    parent_department = Field(attribute='parent_department', column_name=Department.parent_department.field.verbose_name)
    department_name = Field(attribute='department_name', column_name=Department.department_name.field.verbose_name)
    department_id = Field(attribute='department_id', column_name=Department.department_id.field.verbose_name)
    class Meta:
        model = Department
        # fields 匯入時要求的欄位格式
        # fields = ()
        exclude = ['modified_by','id','created_date','update_date']
        # export_order = ('parent_department','department_name','department_id')

class ProjectConfirmationResource(resources.ModelResource):
    id = Field(attribute='id', column_name="編號", widget=ConfirmationIDWidget())
    quotation_id = Field(attribute='quotation_id', column_name=Project_Confirmation.quotation_id.field.verbose_name)
    project_name = Field(attribute='project_name', column_name=Project_Confirmation.project_name.field.verbose_name)
    order_id = Field(attribute='order_id', column_name=Project_Confirmation.order_id.field.verbose_name)
    c_a = Field(attribute='c_a', column_name=Project_Confirmation.c_a.field.verbose_name)
    client = Field(attribute='client', column_name=Project_Confirmation.client.field.verbose_name)
    requisition = Field(attribute='requisition', column_name=Project_Confirmation.requisition.field.verbose_name)
    turnover = Field(attribute='turnover', column_name=Project_Confirmation.turnover.field.verbose_name)
    is_completed = Field(attribute='is_completed', column_name=Project_Confirmation.is_completed.field.verbose_name, widget=BooleanWidget())
    completion_report_employee = Field(attribute='completion_report_employee', column_name=Project_Confirmation.completion_report_employee.field.verbose_name)
    completion_report_date = Field(attribute='completion_report_date', column_name=Project_Confirmation.completion_report_date.field.verbose_name)
    remark = Field(attribute='remark', column_name=Project_Confirmation.remark.field.verbose_name)
    attachment = Field(attribute='attachment', column_name=Project_Confirmation.attachment.field.verbose_name)
    created_by = Field(attribute='created_by', column_name=Project_Confirmation.created_by.field.verbose_name)

    class Meta:
        model = Project_Confirmation
        exclude = ['modified_by','created_date','update_date','Approval']
        
    # 命名方式為 dehydrate_欄位，匯出到此欄位就會呼叫這個方法轉成超連結
    def dehydrate_attachment(self, instance):
        if instance.attachment:
            base_url = settings.BASE_URL
            attachment_url = base_url + instance.attachment.url
            return '=HYPERLINK("%s", "%s")' % (attachment_url, instance.attachment.name)
        else:
            return ""

class ProjectJobAssignResource(resources.ModelResource):
    id = Field(attribute='id', column_name="編號", widget=JobAssignIDWidget())
    project_confirmation = Field(attribute='project_confirmation', column_name=Project_Job_Assign.project_confirmation.field.verbose_name)
    # job_assign_id = Field(attribute='job_assign_id', column_name=Project_Job_Assign.job_assign_id.field.verbose_name)
    attendance_date = Field(attribute='attendance_date', column_name=Project_Job_Assign.attendance_date.field.verbose_name)
    work_employee = Field(attribute='work_employee', column_name=Project_Job_Assign.work_employee.field.verbose_name)
    lead_employee = Field(attribute='lead_employee', column_name=Project_Job_Assign.lead_employee.field.verbose_name)
    vehicle = Field(attribute='vehicle', column_name=Project_Job_Assign.vehicle.field.verbose_name)
    location = Field(attribute='location', column_name=Project_Job_Assign.location.field.verbose_name)
    project_type = Field(attribute='project_type', column_name=Project_Job_Assign.project_type.field.verbose_name)
    remark = Field(attribute='remark', column_name=Project_Job_Assign.remark.field.verbose_name)
    created_by = Field(attribute='created_by', column_name=Project_Job_Assign.created_by.field.verbose_name)

    class Meta:
        model = Project_Job_Assign
        exclude = ['modified_by', 'created_date','update_date','Approval']

class ProjectEmployeeAssignResource(resources.ModelResource):
    id = Field(attribute='id', column_name="編號", widget=EmployeeAssignIDWidget())
    project_job_assign = Field(attribute='project_job_assign', column_name=Project_Employee_Assign.project_job_assign.field.verbose_name)
    construction_date = Field(attribute='construction_date', column_name=Project_Employee_Assign.construction_date.field.verbose_name)
    completion_date = Field(attribute='completion_date', column_name=Project_Employee_Assign.completion_date.field.verbose_name)
    is_completed = Field(attribute='is_completed', column_name=Project_Employee_Assign.is_completed.field.verbose_name, widget=BooleanWidget())
    construction_location = Field(attribute='construction_location', column_name=Project_Employee_Assign.construction_location.field.verbose_name)
    inspector = Field(attribute='inspector', column_name=Project_Employee_Assign.inspector.field.verbose_name)
    manuscript_return_date = Field(attribute='manuscript_return_date', column_name=Project_Employee_Assign.manuscript_return_date.field.verbose_name)
    lead_employee = Field(attribute='lead_employee', column_name=Project_Employee_Assign.lead_employee.field.verbose_name)
    enterprise_signature = Field(attribute='enterprise_signature', column_name=Project_Employee_Assign.enterprise_signature.field.verbose_name)
    carry_equipments = Field(attribute='carry_equipments', column_name=Project_Employee_Assign.carry_equipments.field.verbose_name)
    created_by = Field(attribute='created_by', column_name=Project_Employee_Assign.created_by.field.verbose_name)

    class Meta:
        model = Project_Employee_Assign
        exclude = ['modified_by','created_date','update_date','Approval']