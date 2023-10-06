from datetime import date, timedelta
from .models import Travel_Application,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail,Leave_Param,Leave_Application, Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
from urllib.parse import parse_qs
from django.forms.models import model_to_dict
from django.conf import settings

from openpyxl import load_workbook
from django.db.models import Sum



def salaryFile(get_salary,get_type):
    title = ""
    if get_type:
        title = "薪資條"
    else:
        title = "激勵性獎金"

    get_details = get_salary.details.all()
    file_path = 'static/files/salary_template.xlsx'

    try:
        workbook = load_workbook(filename=file_path)
    except Exception as e:
        return True,"檔案位置發生問題"

    year,month,user = get_salary.year, get_salary.month,get_salary.user
    full_name,employee_id=user.full_name,user.employee_id,
    departments_name = ""
    if user.departments:
        departments_name = user.departments.department_name

    sheet = workbook.active
    
    deduction_items = get_details.filter(deduction=True,five=get_type)
    addition_items = get_details.filter(deduction=False,five=get_type)
    deduction_sum = deduction_items.aggregate(total=Sum('adjustment_amount'))['total'] or 0
    addition_sum = addition_items.aggregate(total=Sum('adjustment_amount'))['total'] or 0
    difference = addition_sum - deduction_sum

    print(full_name,deduction_sum,addition_sum,difference)

    #http://localhost:8000/restful/salaryfile/2023/10/2/1
    try:
        for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            
            for index, cell_value in enumerate(row, start=1):
                if cell_value == "YM":
                    sheet.cell(row=i, column=index, value=f"{year}年{month}月")
       
                if cell_value == "Title":
                    sheet.cell(row=i, column=index, value=title)
                elif cell_value == "E_ID":
                    sheet.cell(row=i, column=index, value=employee_id)
                elif cell_value == "D_SUM":
                    sheet.cell(row=i, column=index, value=addition_sum)
                elif cell_value == "D_COST":
                    sheet.cell(row=i, column=index, value=deduction_sum)
                elif cell_value == "D_RESULT":
                    sheet.cell(row=i, column=index, value=difference)
                elif cell_value == "DT":
                    sheet.cell(row=i, column=index, value=departments_name)
                elif cell_value == "NAME":
                    sheet.cell(row=i, column=index, value=full_name)
                if cell_value == "ADD_LIST":
                    if  len(addition_items)==0:
                        sheet.cell(row=i, column=index, value="")
                        sheet.cell(row=i, column=index+1, value="")
                    else:
                        for next_index, item in enumerate(addition_items):
                            sheet.cell(row=i+next_index, column=index, value= item.name)
                            sheet.cell(row=i+next_index, column=index+1, value=item.adjustment_amount)
                if cell_value == "COST_LIST":
                    if  len(deduction_items)==0:
                        sheet.cell(row=i, column=index, value="")
                        sheet.cell(row=i, column=index+1, value="")
                    else:
                        for next_index, item in enumerate(deduction_items):
                            sheet.cell(row=i+next_index, column=index, value= item.name)
                            sheet.cell(row=i+next_index, column=index+1, value=item.adjustment_amount)

    except ValueError as e:
        return True,"遇到欄位合併的錯誤"
    except Exception as e: 
        return True,"系統無法分析此樣板，出現意外錯誤"

    new_file=f"media/salary_files/{full_name}_{employee_id}_{title}.xlsx"
    workbook.save(new_file)
    return False,new_file



#
def Check_Permissions(user,name):
    if settings.PASS_TEST_FUNC or user.groups.filter(name__icontains='最高權限').exists() :
        return True
    return user.groups.filter(name__icontains='薪水管理').exists()  
    
#取得當周日期
def get_weekdays(to_week):
    weekdays = []
    today = date.today()
    current_date = today - timedelta(days=today.weekday())
    while current_date.weekday() < to_week:
        weekdays.append(current_date)
        current_date += timedelta(days=1)
    return weekdays 

def get_weekly_clock_data(userid):
    weekdays = get_weekdays(5)
    weekly_clock_data = []

    for weekday in weekdays:        
        clock_records = Clock.objects.filter(clock_date=weekday).filter(employee_id=userid).order_by('clock_time')
        clock_in_records = []
        clock_out_records = []
        for record in clock_records:

            if record.type_of_clock =="2":
                get_approval = record.clock_correction.all()[0].Approval
                if get_approval :
                    if get_approval.current_status =="completed":
                        if record.clock_in_or_out:
                            clock_in_records.append(record)   
                        else:         
                            clock_out_records.append(record)   
            else:
                if record.clock_in_or_out:
                    clock_in_records.append(record)   
                else:         
                    clock_out_records.append(record)   

        if len(clock_in_records)==0:
            check_in = ""
        else:
            check_in =clock_in_records[0].clock_time.strftime('%H:%M') 

        if len(clock_out_records)==0:
            check_out = ""
        else:
            check_out = clock_out_records[-1].clock_time.strftime('%H:%M') 


      
        daily_data = {
            'day': weekday.strftime('%m/%d'),
            'checkin': check_in,
            'checkout': check_out
        }
        weekly_clock_data.append(daily_data)
    return weekly_clock_data

def convent_employee(employees):
    employee_ary=[]
    selected_fields = ['id','full_name']
    for get_employee in employees:
        employee_dict = model_to_dict(get_employee,fields=selected_fields)
        
        # del employee_dict["uploaded_files"]
        # if "profile_image" in employee_dict:
        #     if  employee_dict['profile_image']:
        #         employee_dict['profile_image'] = employee_dict["profile_image"].url
        #     else:
        #         employee_dict['profile_image'] = None       
        employee_ary.append(employee_dict)
    return employee_ary


def convent_dict(data):
    data_str = data.decode('utf-8')
    dict_data = parse_qs(data_str)
    print(dict_data)
    print("convent")
    if "csrfmiddlewaretoken" in dict_data:
        del dict_data["csrfmiddlewaretoken"]


    new_dict_data = {}
    for key, value in dict_data.items():
        new_dict_data[key] = value[0]
        process_key =("inspector","support_employee","work_item","carry_equipments","user_set","completion_report_employee","work_employee","lead_employee","completion_report_employeeS")
        if key in process_key: #處理員工多對多陣列        
            new_dict_data[key] =  [int(num) for num in  value]
        elif  key == "test_items":           
            new_dict_data[key] =[num for num in  value]
        else:            
            match  value[0]:
                case "true":
                    new_dict_data[key] = True               
                case "false":
                    new_dict_data[key] =False
                case _:
                    new_dict_data[key] = value[0]
    print(new_dict_data)
    return new_dict_data


def convent_excel_dict(worksheet,model):
    template_dict={}
    convent_model= None
    print("model: ",model)
    match  model:
        case "project-confirmation":
            template_dict= {
                "quotation_id":"",
                "project_confirmation_id":"",
                "c_a":"",
                "project_name":"",
                "client":"",
                "requisition":"",
                "order_id":"",
                "turnover":"",
            }
            convent_model=Project_Confirmation
        case "job-assign":
            template_dict= {
                "job_assign_id":"",
                "attendance_date":"",
                "location":"",
                "project_type":"",
                "remark":"",
            }
            convent_model=Project_Job_Assign
        case "employee-assign":
            template_dict= {
                "construction_date":"",
                "completion_date":"",
                "is_completed":"",
                "construction_location":"",
            }
            convent_model=Project_Employee_Assign
        case _:
            return "error"

    convent_ary=[]
    pass_one =True
    for row in worksheet.iter_rows():
        if pass_one:
            pass_one =False
            continue
            
        new_dict = template_dict.copy()
        for i, key in enumerate(new_dict.keys()):
            print(row[i])
            print(row[i].value)
            new_dict[key] = row[i].value
        
        #防止全空白+入
        all_values_are_none_or_blank = all(value is None or value == '' for value in new_dict.values())
        if not all_values_are_none_or_blank: 
            convent_ary.append(new_dict)

    return convent_ary,convent_model

def get_model_by_name(model_name):
     match model_name:
        case "project_confirmation":
            return Project_Confirmation
        case "job_assign":
            return Project_Job_Assign
        case "Project_Employee_Assign":
            return Project_Employee_Assign
        case "Work_Overtime_Application":
            return Work_Overtime_Application
        case "Leave_Application":
             return Leave_Application
        case "Clock_Correction_Application":
             return Clock_Correction_Application
        case "Travel_Application":
             return Travel_Application
        case _:
            return None

def match_excel_content(model):
    match  model:
        case "project-confirmation":
            print("project-confirmation")
        case "job-assign":
            print("job-assign")
        case "employee-assign":
            print("employee-assign")
        case _:
            return "error"
    