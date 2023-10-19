from datetime import date, timedelta
from Backend.models import Employee,Travel_Application,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail,Leave_Param,Leave_Application, Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
from urllib.parse import parse_qs
from django.forms.models import model_to_dict
from django.conf import settings
from django.http import HttpResponse
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle
from urllib.parse import quote
import os
from django.db.models import Sum
import math
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill




def employeeAssignFile(employee_assign_obj):

    client = "" if employee_assign_obj.project_job_assign.project_confirmation.quotation.client is None else employee_assign_obj.project_job_assign.project_confirmation.quotation.client
    quotation_id = "" if employee_assign_obj.project_job_assign.project_confirmation.quotation.quotation_id is None else employee_assign_obj.project_job_assign.project_confirmation.quotation.quotation_id
    construction_date = "" if employee_assign_obj.construction_date is None else employee_assign_obj.construction_date
    requisition = "" if employee_assign_obj.project_job_assign.project_confirmation.quotation.requisition is None else employee_assign_obj.project_job_assign.project_confirmation.quotation.requisition
    # order_id = employee_assign_obj.requisition.contact_person or ""
    completion_date =  employee_assign_obj.completion_date  or ""
    project_name = employee_assign_obj.project_job_assign.project_confirmation.quotation.project_name or ""
    location = employee_assign_obj.project_job_assign.location or ""  
    manuscript_return_date = employee_assign_obj.manuscript_return_date or ""


    file_path = r'media/system_files/employee_assign_template.xlsx'
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active

    try:
        for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            
            for index, cell_value in enumerate(row, start=1):
                if cell_value == "CLIENT":
                    sheet.cell(row=i, column=index, value=str(client))
                elif cell_value == "QUOTATION_ID":
                    sheet.cell(row=i, column=index, value=quotation_id)
                elif cell_value == "CONSTRUCTION_DATE":
                    sheet.cell(row=i, column=index, value=construction_date)
                elif cell_value == "REQUISITION":
                    sheet.cell(row=i, column=index, value=str(requisition))
                elif cell_value == "COMPLETION_DATE":
                    sheet.cell(row=i, column=index, value=completion_date)
                elif cell_value == "PROJECT_NAME":
                    sheet.cell(row=i, column=index, value=project_name)
                elif cell_value == "LOCATION":
                    sheet.cell(row=i, column=index, value=location)
                elif cell_value == "MANUSCRIPT_RETURN_DATE":
                    sheet.cell(row=i, column=index, value=manuscript_return_date)
                # elif cell_value == "ITEM_LIST":
                #     if  len(item_list)==0:
                #         sheet.cell(row=i, column=index, value="")
                #         sheet.cell(row=i, column=index+1, value="")
                #         sheet.cell(row=i, column=index+5, value="")
                #         sheet.cell(row=i, column=index+6, value="")
                #         sheet.cell(row=i, column=index+7, value="")
                #         sheet.cell(row=i, column=index+8, value="")
                #     else:
                #         for next_index, item in enumerate(item_list): #艾利克
                #             sheet.cell(row=i+next_index, column=index, value= next_index+1)
                #             sheet.cell(row=i+next_index, column=index+1, value=item.work_item.item_name)
                #             sheet.cell(row=i+next_index, column=index+5, value=item.work_item.contract_id)
                #             sheet.cell(row=i+next_index, column=index+6, value=item.work_item.unit)
                #             num =item.number
                #             money=item.work_item.money()
                #             item_total_moeny=0
                #             if str(money).isnumeric():
                #                 item_total_moeny = num*money
                #             sheet.cell(row=i+next_index, column=index+7, value=num)
                #             sheet.cell(row=i+next_index, column=index+8, value=money )
                #             sheet.cell(row=i+next_index, column=index+9, value=item_total_moeny )
                #             sum+=item_total_moeny
                # elif cell_value == "SUM":
                #     sheet.cell(row=i, column=index, value=sum)
                # elif cell_value == "hide_key":
                #     if see:
                #         sheet.cell(row=i, column=index, value="客戶名稱").fill = grey_fill
                #     else:
                #         sheet.cell(row=i, column=index, value="")
                # elif cell_value == "hide_name":
                #     if five:
                #         sheet.cell(row=i, column=index, value=hide_client)
                #     else:

                #         if see:
                #             sheet.cell(row=i, column=index, value=hide_client).fill = grey_fill
                #         else:
                #             sheet.cell(row=i, column=index, value="")
                # elif cell_value == "sum_five":
                #     if five:                           
                #         five_sum = math.ceil(sum *0.05)
                #     else: 
                #         five_sum=0
                #     sheet.cell(row=i, column=index, value=five_sum)
                # elif cell_value == "all_sum":
                #     all_sum = sum + five_sum
                #     sheet.cell(row=i, column=index, value=all_sum)

    except ValueError as e:
        return True,"遇到欄位合併的錯誤"
    except Exception as e: 
        print(e)
        return True,"系統無法分析此樣板，出現意外錯誤"

    filename = f"【派工單】 {employee_assign_obj}-{requisition}-{project_name}.xlsx"
    quoted_filename = quote(filename)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] =  f'attachment; filename="{quoted_filename}"'
    workbook.save(response)
    return response
