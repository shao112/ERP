from datetime import date, timedelta
from .models import Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
from urllib.parse import parse_qs
from django.forms.models import model_to_dict

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
        clock_records = Clock.objects.filter(created_date=weekday).filter(employee_id=userid).order_by('clock_time')
        check_in = clock_records.first().clock_time.strftime('%H:%M') if clock_records else ''
        check_out = clock_records.last().clock_time.strftime('%H:%M') if clock_records and len(clock_records) > 1 else ""
            # check_out = clock_records.last().clock_time.strftime('%H:%M') if clock_records else ''
        daily_data = {
            'day': weekday.strftime('%m%d'),
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
        else:            
            match  value[0]:
                case "true":
                    new_dict_data[key] = True
                case "false":
                    new_dict_data[key] =False
                case "csrfmiddlewaretoken":
                    pass
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
    