from Backend.models import AnnualLeave,Employee
from datetime import timedelta
from datetime import datetime
import math

def calculate_annual_leave(employee):
    start_work_date = employee.start_work_date
    if not start_work_date:
        return
    
    years = employee.seniority()
    today = datetime.today().date()

    #計算入職的前一天的明年時間
    end_date = employee.start_work_date - timedelta(days=1)
    end_date = end_date.replace(year=today.year + 1)
    if years == "人資單位未填寫入值日" :
        return "人資單位未填寫入值日"

    if years <0.6 :
        return "小於0.6"
    
    if years < 1:
        has_three_days_leave = employee.annualleaves.filter(days=3).exists()
        if not has_three_days_leave:
            annual_leave = AnnualLeave.objects.create(days=3, end_date=end_date, remark="")
            employee.annualleaves.add(annual_leave)
        return "0.6"
    
    #今天=入職 才執行給假
    if  not (today.month == start_work_date.month and today.day == start_work_date.day):
        return "不執行"
    
    give_day = 0
    if years >= 1 and years < 2:
        give_day= 7
    elif years >= 2 and years < 3:
        give_day= 10
    elif years >= 3 and years < 5:
        give_day= 14
    elif years >= 5 and years < 10:
        give_day= 15
    elif years == 10:
        give_day= 16
    else:
        give_day= min(30, math.floor(years))

    annual_leave = AnnualLeave.objects.create(days=give_day, end_date=end_date, remark="")
    employee.annualleaves.add(annual_leave)
    return f"年資:{years}、給假{give_day}"


def calculate_annual_leave_for_all_employees():
    print("go task")
    employees = Employee.objects.all()
    for employee in employees:
        msg = calculate_annual_leave(employee)
        print(employee.full_name)
        print(msg)
