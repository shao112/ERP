from datetime import date, timedelta
from .models import Travel_Application,Clock_Correction_Application, Work_Overtime_Application, Salary,SalaryDetail,Leave_Param,Leave_Application, Clock,Project_Confirmation,Project_Job_Assign,Project_Employee_Assign
from urllib.parse import parse_qs
from django.forms.models import model_to_dict






def create_salary(employee,year,month):
    salary, created = Salary.objects.get_or_create(user=employee, year=year, month=month)
    if not created:#清除所有明細
        SalaryDetail.objects.filter(salary=salary).delete()

    SalaryDetail.objects.create(
        salary=salary,
        name='基本薪資',
        system_amount=employee.default_salary,
        adjustment_amount=employee.default_salary,
        deduction=False
    )

    SalaryDetail.objects.create(
        salary=salary,
        name='伙食加給',
        system_amount=2400,  
        adjustment_amount=2400,
        deduction=False
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
