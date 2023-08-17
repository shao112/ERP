from import_export import resources
from import_export.fields import Field
from .models import Department

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