from datetime import date, timedelta
from .models import LaborHealthInfo,Travel_Application,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail,Leave_Param,Leave_Application, Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
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
        deduction=False,
        five=True,
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='職務加給',
        system_amount=employee.job_addition,
        adjustment_amount=employee.job_addition,
        deduction=False,
        five=True,
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='手機加給',
        system_amount=employee.phone_addition,
        adjustment_amount=employee.phone_addition,
        deduction=False,
        five=True,
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='證照加給',
        system_amount=employee.certificates_addition,
        adjustment_amount=employee.certificates_addition,
        deduction=False,
        five=True,
    )

    #勞建保
    labor_insurance_personal = LaborHealthInfo.get_salary_range(employee.labor_protection,"labor_insurance_personal")
    health_insurance_personal = LaborHealthInfo.get_salary_range(employee.health_insurance,"health_insurance_personal")

    SalaryDetail.objects.create(
        salary=salary,
        name='勞保',
        system_amount=labor_insurance_personal,
        adjustment_amount=labor_insurance_personal,
        deduction=True,
        five=True,
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='健保',
        system_amount=health_insurance_personal,
        adjustment_amount=health_insurance_personal,
        deduction=True,
        five=True,
    )

    labor_pension_moeny =employee.labor_pension_moeny
    get_employee_labor_pension = employee.labor_pension
    SalaryDetail.objects.create(
            salary=salary,
            name='*勞退公提(6%免扣)',
            system_amount=math.ceil(labor_pension_moeny*6/100),
            adjustment_amount= math.ceil(labor_pension_moeny*6/100),
            deduction=True,
        five=True,
    )
    if get_employee_labor_pension >6:
        #自提
        employee_labor_pension_by_self = get_employee_labor_pension-6
        SalaryDetail.objects.create(
            salary=salary,
            name=f'勞退自提({employee_labor_pension_by_self}%)',
            system_amount=math.ceil(labor_pension_moeny*employee_labor_pension_by_self/100),
            adjustment_amount= math.ceil(labor_pension_moeny*employee_labor_pension_by_self/100),
            deduction=True,
        five=True,
        )





    print("加班費")
    weekdays_overtime = Work_Overtime_Application.get_money_by_user_month(employee,year=year,month=month)
    overtime_pay=weekdays_overtime.get("overtime_pay")#
    work_allowance=weekdays_overtime.get("work_allowance")

    SalaryDetail.objects.create(
            salary=salary,
            name="免稅加班",
            system_amount=overtime_pay,  
            adjustment_amount=overtime_pay,
            deduction=False,
        five=False,
        )
    
    SalaryDetail.objects.create(
            salary=salary,
            name="工作津貼",
            system_amount=work_allowance,  
            adjustment_amount=work_allowance,
            deduction=False,
            five=False,
        )
    
    print("出差 伙食")
    location_money,food_money,_ = Project_Job_Assign.get_month_list_day(employee,year=year,month=month)
    
    SalaryDetail.objects.create(
            salary=salary,
            name="出差津貼",
            system_amount=location_money,  
            adjustment_amount=location_money,
            deduction=False,
        five=False,            
        )
    
    SalaryDetail.objects.create(
            salary=salary,
            name="伙食津貼",
            system_amount=food_money,  
            adjustment_amount=food_money,
            deduction=False,
        five=False,            
        )

    print("車程津貼")
    _,tr_cost,_ = Travel_Application.get_time_cost_details_by_YM(employee,year=year,month=month)
    SalaryDetail.objects.create(
            salary=salary,
            name="車程津貼",
            system_amount=tr_cost,  
            adjustment_amount=tr_cost,
            deduction=False,
        five=False,            
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
            deduction=True,
                    five=True,            
        )
