from import_export import resources, fields,widgets
from import_export.fields import Field

from django.conf import settings # 要取得 BASE_URL

from .models import Department, Project_Confirmation

# 匯出布林值欄位只會顯示 1 跟 0，要特別處理布林值
class BooleanWidget(widgets.BooleanWidget):
    def render(self, value, obj):
        if value in self.NULL_VALUES:
            return ""
        return '是' if value else '否'

class DepartmentResource(resources.ModelResource):
    belong_to_company = Field(attribute='belong_to_company', column_name=Department.belong_to_company.field.verbose_name)
    parent_department = Field(attribute='parent_department', column_name=Department.parent_department.field.verbose_name)
    department_name = Field(attribute='department_name', column_name=Department.department_name.field.verbose_name)
    department_id = Field(attribute='department_id', column_name=Department.department_id.field.verbose_name)
    # def get_export_fields(self):
    #     fields = self.get_fields()
    #     for field in fields:
    #         field_name = self.get_field_name(field)
    #         # 如果有设置 verbose_name，则将 column_name 替换为 verbose_name, 否则维持原有的字段名。
    #         if field_name in self.verbose_name_dict.keys():
    #             field.column_name = self.verbose_name_dict[field_name]
    #     return fields
    class Meta:
        model = Department
        # fields 匯入時要求的欄位格式
        # fields = ()
        exclude = ['modified_by','id','created_date','update_date']
        # export_order = ('parent_department','department_name','department_id')

class ProjectConfirmationResource(resources.ModelResource):
    project_confirmation_id = Field(attribute='project_confirmation_id', column_name=Project_Confirmation.project_confirmation_id.field.verbose_name)
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
    Approval = Field(attribute='Approval', column_name=Project_Confirmation.Approval.field.verbose_name)
    created_by = Field(attribute='created_by', column_name=Project_Confirmation.created_by.field.verbose_name)

    class Meta:
        model = Project_Confirmation
        exclude = ['modified_by','id','created_date','update_date']
        
    # 命名方式為 dehydrate_欄位，匯出到此欄位就會呼叫這個方法轉成超連結
    def dehydrate_attachment(self, instance):
        if instance.attachment:
            base_url = settings.BASE_URL
            attachment_url = base_url + instance.attachment.url
            return '=HYPERLINK("%s", "%s")' % (attachment_url, instance.attachment.name)
        else:
            return ""