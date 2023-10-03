from datetime import date, timedelta
from .models import Travel_Application,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail,Leave_Param,Leave_Application, Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
from urllib.parse import parse_qs
from django.forms.models import model_to_dict

import math




def create_salary(employee,year,month):
    salary, created = Salary.objects.get_or_create(user=employee, year=year, month=month)
    if not created:#清除所有明細
        SalaryDetail.objects.filter(salary=salary).delete()

    #基本項目
    SalaryDetail.objects.create(
        salary=salary,
        name='基本薪資',
        system_amount=employee.default_salary,
        adjustment_amount=employee.default_salary,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='職務加給',
        system_amount=employee.job_addition,
        adjustment_amount=employee.job_addition,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='手機加給',
        system_amount=employee.phone_addition,
        adjustment_amount=employee.phone_addition,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='伙食津貼',
        system_amount=employee.food_addition,
        adjustment_amount=employee.food_addition,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='證照加給',
        system_amount=employee.certificates_addition,
        adjustment_amount=employee.certificates_addition,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='勞保',
        system_amount=employee.labor_protection,
        adjustment_amount=employee.labor_protection,
        deduction=True
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='健保',
        system_amount=employee.health_insurance,
        adjustment_amount=employee.health_insurance,
        deduction=True
    )

    SalaryDetail.objects.create(
        salary=salary,
        name=f'勞退({employee.labor_pension}%)',
        system_amount=math.ceil(employee.default_salary*employee.labor_pension/100),
        adjustment_amount= math.ceil(employee.default_salary*employee.labor_pension/100),
        deduction=True
    )






    print("加班費")
    work_moeny ,_ = Work_Overtime_Application.get_money_by_user_month(employee,year=year,month=month)
    SalaryDetail.objects.create(
            salary=salary,
            name="加班費",
            system_amount=work_moeny,  
            adjustment_amount=work_moeny,
            deduction=False
        )
    
    print("出差 伙食")
    location_money,food_money,_ = Project_Job_Assign.get_month_list_day(employee,year=year,month=month)
    
    SalaryDetail.objects.create(
            salary=salary,
            name="出差津貼",
            system_amount=location_money,  
            adjustment_amount=location_money,
            deduction=False
        )
    
    SalaryDetail.objects.create(
            salary=salary,
            name="伙食津貼",
            system_amount=food_money,  
            adjustment_amount=food_money,
            deduction=False
        )

    print("車程津貼")
    _,tr_cost,_ = Travel_Application.get_time_cost_details_by_YM(employee,year=year,month=month)
    SalaryDetail.objects.create(
            salary=salary,
            name="車程津貼",
            system_amount=tr_cost,  
            adjustment_amount=tr_cost,
            deduction=False
        )
    

    #請假單
    print("請假單")
    cost_list = Leave_Param.get_year_total_cost_list(employee,year=year,month=month)
    for item in cost_list:
        SalaryDetail.objects.create(
            salary=salary,
            name=item['name'],
            system_amount=item['cost'],  
            adjustment_amount=item['cost'],
            deduction=True
        )
