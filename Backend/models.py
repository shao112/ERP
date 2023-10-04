from django.db.models.functions import ExtractYear,ExtractMonth,ExtractDay
import math
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.db import models
from datetime import time
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user
from datetime import date
import os
from datetime import timedelta,datetime

from django.db.models import F, Sum,Q

LOCATION_CHOICES = [
    ("台東", "台東"),
    ("花蓮", "花蓮"),
    ("宜蘭", "宜蘭"),
    ("北北基", "北北基"),
    ("桃園", "桃園"),
    ("新竹", "新竹"),
    ("苗栗", "苗栗"),
    ("台中", "台中"),
    ("南投", "南投"),
    ("彰化", "彰化"),
    ("雲林", "雲林"),
    ("嘉義", "嘉義"),
    ("台南", "台南"),
    ("高雄", "高雄"),
    ("屏東", "屏東"),
    ("花蓮", "花蓮"),
    ("台東", "台東"),
]



class SysMessage(models.Model):
    Target_user = models.ForeignKey("Employee", related_name="sys_messages", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='顯示對象')
    content = models.TextField(verbose_name='內容')
    watch = models.BooleanField(default=False,verbose_name='已看過')

    class Meta:
        verbose_name = '系統消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

class UploadedFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='employee_profile/users/')

    class Meta:
        verbose_name = '檔案上傳管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

from django.core.exceptions import PermissionDenied

#紀錄修改者
class ModifiedModel(models.Model):
    modified_by = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if hasattr(self, 'Approval'):  
            if self.Approval:
                current_status = self.Approval.current_status
                if current_status == 'completed' or current_status == 'in_process':
                    raise PermissionDenied("簽核中或簽核完成禁止刪除")

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        user = get_current_authenticated_user()
        
        if user !=None:
            self.modified_by = user.employee            
            if hasattr(self, 'created_by'):
                if self.created_by ==None:
                    self.created_by =user.employee
 
        super().save(*args, **kwargs)

    def update_fields_and_save(self, **kwargs):
        if hasattr(self, 'Approval'):
            if self.Approval:
                current_status = self.Approval.current_status
                if current_status == 'completed' or current_status == 'in_process':
                    raise PermissionDenied("簽核中或簽核完成禁止修改.")


        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

class ReferenceTable(models.Model):
    location_city_residence = models.CharField(max_length=4, choices=LOCATION_CHOICES, verbose_name="居住地")
    location_city_business_trip = models.CharField(max_length=4, choices=LOCATION_CHOICES, verbose_name="出差地")
    amount = models.DecimalField(verbose_name="錢/單位",max_digits=10, decimal_places=2)
    name=models.CharField(max_length=10)

    class Meta:
        verbose_name = "參照表"
        verbose_name_plural = "參照表"

    def __str__(self):
        return f"{self.name}參照表 居住地 {self.location_city_residence} / 出差地 {self.location_city_business_trip}  金額 {self.amount}"


        
# 員工（以內建 User 擴增）
class Employee(ModifiedModel):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A', 'A型'),
        ('B', 'B型'),
        ('AB','AB型'),
        ('O', 'O型'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('M', '已婚'),
        ('S', '未婚'),
        ('D', '離異'),
    ]
    MILITARY_STATUS_CHOICES = [
        ('M', '義務役'),
        ('E', '免服役'),
        ('A', '替代役'),
    ]   
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='employee_profile/', blank=True, null=True, default='employee_profile/default_profile.png', verbose_name='員工照片')
    location_city = models.CharField(max_length=4, choices=LOCATION_CHOICES, null=True, blank=True, verbose_name='居住城市(用於計算)')
    uploaded_files = models.ManyToManyField(UploadedFile,blank=True,  related_name="userfile")
    full_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='員工名稱')
    employee_id	 = models.CharField(max_length=30, blank=True,verbose_name='員工編號')
    departments = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='employees', verbose_name='部門名稱')# 你可以通过department.employees.all()访问一个部门的所有员工。
    position = models.CharField(max_length=30, null=True, blank=True, verbose_name='職稱')
    phone_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='手機號碼')
    contact_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='聯絡電話')
    start_work_date = models.DateField(null=True, blank=True, verbose_name='到職日期')
    seniority = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='目前年資')
    id_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='身份證字號')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='性別')
    blood_type = models.CharField(max_length=2, choices=BLOOD_TYPE_CHOICES, null=True, blank=True, verbose_name='血型')
    birth_place = models.CharField(max_length=100, null=True, blank=True, verbose_name='出生地')
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True, blank=True, verbose_name='婚姻狀況')
    military_status = models.CharField(max_length=1, choices=MILITARY_STATUS_CHOICES, null=True, blank=True, verbose_name='兵役狀況')
    permanent_address = models.CharField(max_length=50, null=True, blank=True, verbose_name='戶籍地址')
    current_address_city = models.CharField(max_length=50, null=True, blank=True, verbose_name='現居地址縣市')
    current_address = models.CharField(max_length=50, null=True, blank=True, verbose_name='現居地址')
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name='所在地')
    company_email = models.EmailField(null=True, blank=True, verbose_name='公司E_Mail')
    personal_email = models.EmailField(null=True, blank=True, verbose_name='個人E_Mail')
    emergency_contact = models.CharField(max_length=50, null=True, blank=True, verbose_name='緊急聯絡人1')
    emergency_contact_relations = models.CharField(max_length=50, null=True, blank=True, verbose_name='關係1')
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='聯絡人電話1')
    default_salary = models.PositiveIntegerField(default=26000, null=True, blank=True, verbose_name="基本薪資")
    job_addition = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="職務加給")
    phone_addition = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="手機加給")
    food_addition = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="伙食津貼")
    certificates_addition = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="證照加給")
    labor_protection = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="勞保")
    health_insurance = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="健保")
    labor_pension = models.PositiveIntegerField(default=6, null=True, blank=True, verbose_name="勞退比例(%)")

    class Meta:
        verbose_name = "員工"   # 單數
        verbose_name_plural = verbose_name   #複數

    def get_hour_salary(self):
        return  math.ceil(self.default_salary / 240)


    def day_status(self, date): #當天還要上幾小時

        leave_applications = self.leave_list.filter(
            start_date_of_leave__lte=date,
            end_date_of_leave__gte=date,
            Approval__current_status="completed"
        )
        total_hour = 8
        total_minutes = 0
        cost_minutes = 0
        results = []
            
        for leave_application in leave_applications:
            result = leave_application.hour_day(date)
            total_hour -= result["total_hours"]
            cost_minutes += result["total_minutes"]
            results.append(result)       
        
        total_hour -= cost_minutes // 60
        cost_minutes= cost_minutes%60
        if cost_minutes == 30:
            total_hour-=1
            total_minutes=30
        
        # if results!=[]:
        #     print(results)

        return total_hour,total_minutes ,results
    
    def __str__(self):
        return f"{self.full_name}"


class SalaryDetail(models.Model):
    salary = models.ForeignKey("Salary",related_name="details",on_delete=models.CASCADE, verbose_name="依附薪資單",null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='名稱')
    system_amount = models.PositiveIntegerField(default=0, verbose_name='系統金額')
    adjustment_amount = models.PositiveIntegerField(default=0, verbose_name='調整金額')
    deduction = models.BooleanField(default=False, verbose_name='扣款項目') #T是扣項，F是加項
    tax_deduction = models.BooleanField(default=False, verbose_name='應稅項目') #T是扣項，F是加項
    def save(self, *args, **kwargs):  
        if self.system_amount != 0:
            super().save(*args, **kwargs)

    def set_name_and_adjustment_amount(self, name, amount,deduction,tax_deduction):
        self.name = name
        self.deduction = deduction
        self.adjustment_amount = amount
        self.tax_deduction = tax_deduction
        self.save()

    class Meta:
        verbose_name = "薪資明細"
        verbose_name_plural = "薪資明細"

    def __str__(self):
        return f"{self.name} + {self.salary}"


class Salary(ModifiedModel):
    user = models.ForeignKey(Employee,related_name="salary_user" ,on_delete=models.DO_NOTHING, verbose_name="員工")
    year = models.PositiveIntegerField(verbose_name="年")
    month = models.PositiveIntegerField(verbose_name="月")
    created_by = models.ForeignKey("Employee",related_name="Salary_author", on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def system_total_money(self):
        return self.calculate_total_amount()

    @property
    def adjustment_total_money(self):
        return self.calculate_total_amount(False)


    def calculate_adjustment_addition(self):
        details = self.details.filter(deduction=False)
        total_adjustment_addition = details.aggregate(total=Sum(F('adjustment_amount')))['total'] or 0

        return total_adjustment_addition

    def calculate_adjustment_deduction(self):
        details = self.details.filter(deduction=True)
        total_adjustment_deduction = details.aggregate(total=Sum(F('adjustment_amount')))['total'] or 0
        return total_adjustment_deduction


    def calculate_total_amount(self, use_system_amount=True):
        details = self.details.all()
        
        total_amount = 0

        for detail in details:
            if use_system_amount:
                amount_to_add = detail.system_amount
            else:
                amount_to_add = detail.adjustment_amount

            if detail.deduction:
                amount_to_add = -amount_to_add  

            total_amount += amount_to_add
        # print(total_amount)
        return total_amount

    class Meta:
        verbose_name = "薪資"
        verbose_name_plural = "薪資"

    def __str__(self):
        return f"{self.user} - {self.year}年{self.month}月的薪資"



class ApprovalLog(models.Model):
    approval = models.ForeignKey("ApprovalModel", on_delete=models.CASCADE, related_name='approval_logs')
    user = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, verbose_name='簽核者')
    content = models.TextField(blank=True, null=True, verbose_name='內容')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')

    class Meta:
        verbose_name = '簽核記錄'
        verbose_name_plural = '簽核記錄'



class Approval_Target(models.Model):
    STATUS_CHOICES = [
        ('Project_Employee_Assign', '派工單'),
        ('Leave_Application', '請假單'),
        ('Work_Overtime_Application', '加班單'), #這個value會對應下面的value
        ('Clock_Correction_Application', '補卡單'),
        ('Travel_Application', '車程津貼單'),
    ]
    name =models.CharField(max_length=30,verbose_name="表單名稱",choices=STATUS_CHOICES)
    approval_order = models.JSONField(null=True, verbose_name="員工簽核順序")#儲存員工ID、各自主管(X)
    class Meta:
        verbose_name = '簽核流程管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_name_display()}"
    
    def employeeid_to_employee(self):
        employee_array = []
        for approval_order_id in self.approval_order:
            if approval_order_id !="x":
                employee = Employee.objects.get(id=approval_order_id)
                employee_array.append(employee)
            
        return employee_array


class ApprovalModel(models.Model):
    STATUS_CHOICES = [
        ('completed', '完成'),
        ('in_progress', '進行中'),
        ('rejected', '駁回'),
    ]

    #related_name 關聯
    RELATED_NAME_MAP = {
        'Project_Employee_Assign': 'Project_Employee_Assign_Approval',
        'Leave_Application': 'Leave_Application_Approval',
        'Work_Overtime_Application':"Work_Overtime_Application_Approval",
        'Clock_Correction_Application':"Clock_Correction_Application_Approval",
        'Travel_Application':"Travel_Application_Approval",
    }

    #對應的model api 網址，會帶入data-model
    Modal_URL__MAP = {
        'Project_Employee_Assign': 'project_employee_assign',
        'Leave_Application': 'leave_application',
        'Work_Overtime_Application': 'work_overtime_application',
        'Clock_Correction_Application': 'clock_correction_application',
        'Travel_Application': 'Travel_Application',
    }


    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='in_progress')
    #目前待簽index
    current_index = models.IntegerField( verbose_name="待簽核index",default=0,blank=True,null=True)
    #簽核流程
    order =  models.JSONField(null=True, verbose_name="員工簽核順序")#儲存員工ID、各自主管(X)
    #依附簽核
    target_approval = models.ForeignKey(Approval_Target,verbose_name="依附簽核",blank=True,null=True, on_delete=models.CASCADE, related_name='approvals')

    @property
    def model_url(self):
        related_name = self.Modal_URL__MAP.get(self.target_approval.name)
        if related_name:
            return related_name
        return None

    @property
    def get_created_by(self):
        get_foreignkey = self.get_foreignkey()   
        if get_foreignkey:   
            return get_foreignkey.created_by
        return None    

    def send_message_to_related_users(self, content):
            senders = {self.get_created_by}

            for employee_id in self.order:
                if employee_id == "x":
                    department_employees = self.get_created_by.departments.employees.filter(user__groups__name='主管')
                    senders.update(department_employees)
                else:
                    try:
                        employee = Employee.objects.get(id=employee_id)
                        senders.add(employee)
                    except Employee.DoesNotExist:
                        continue

            for sender in senders:
                SysMessage.objects.create(
                    Target_user=sender,
                    content=content
                )

    
    #回傳關聯
    def get_foreignkey(self):
        # print("self.target_approval.name: ",self.target_approval.name)
        related_name = self.RELATED_NAME_MAP.get(self.target_approval.name)
        if related_name:
            getobj = getattr(self, related_name, None).all()
            # print("getobj: ",getobj)
            if  getobj:
                # print("getattr(self, related_name, None).all()[0]: ",getattr(self, related_name, None).all()[0])
                return getattr(self, related_name, None).all()[0]
            return None
        else:
            print("error 找不到對應的related_name")
        return None
    


    def get_approval_employee(self):
        current_index= self.current_index
        approval_order = self.order
        if approval_order==None or  current_index > len(approval_order)-1 :
            return "clean"
        if approval_order[current_index] !="x":
            return Employee.objects.get(id=approval_order[current_index])
        return "x"

    def update_department_status(self, new_status):
        if new_status == 'approved':
            self.find_and_update_parent_department()
        else:
            self.current_status = new_status
            self.save()

    def find_and_update_parent_department(self):
        current_index = self.current_index
        approval_order = self.order
        
        #判斷是不是最後一個
        if current_index ==len(approval_order)-1 :
            self.update_department_status("completed")
            employee_id = self.target_approval
            employee = self.get_created_by
            SysMessage.objects.create(Target_user=employee,content=f"您的 {self.target_approval.get_name_display()} 簽核完畢")
        else:
            current_index+=1            
            employee_id = approval_order[current_index]
            if employee_id =="x":
                senders = self.get_created_by.departments.employees.filter(user__groups__name='主管')
                for sender in senders:
                    SysMessage.objects.create(Target_user=sender,content=f"您有一筆 {self.target_approval.get_name_display()} 單需要簽核")
            else:
                employee = Employee.objects.get(id=employee_id)
                SysMessage.objects.create(Target_user=employee,content=f"您有一筆 {self.target_approval.get_name_display()} 需要簽核")
            self.current_index = current_index
            self.save()

    def get_approval_log_list(self):
        """
        取得相關的 ApprovalLog 並整理成列表
        """
        get_approval_logs = self.approval_logs.all().order_by('id')  # 根據 ID 順序排序
        # print("get_approval_logs: ",get_approval_logs)
        show_list = []
        current_index = self.current_index
        approval_order = self.order
        
        for _, log in enumerate(get_approval_logs): #處理簽過LOG
            show_list.append({
                "show_name": log.user.full_name,
                "department": log.user.departments.department_name,
                "department_pk": log.user.departments.pk,
                "content": log.content, 
                "status": "pass"
            })


        #當到最大數量且 已完成
        if current_index == len(approval_order)-1 and self.current_status == "completed":
            return show_list

        for  employee_id in approval_order[current_index:]:
            show_name= ""
            if employee_id == "x":
                    get_department_name = self.get_created_by.departments.department_name
                    show_name = get_department_name+"(主管待簽)"
            else:
                get_Employee = Employee.objects.get(id=employee_id)
                show_name = get_Employee.full_name

            show_list.append({
                    "user_full_name": None,
                    "user_department": None,
                    "content": None,
                    "show_name":show_name,
                    "status": "wait",
                })
        # print("show_list: ",show_list)
        return show_list

    class Meta:
        verbose_name = '簽核執行'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        try:
            get_foreignkey = self.get_foreignkey()
            get_show_id =""
            get_created_by =""
            if get_foreignkey !="":
                get_show_id = get_foreignkey.get_show_id()
                get_created_by =get_foreignkey.created_by
            
            return f"{self.target_approval.name} - {get_created_by} - {get_show_id}"
        except:
            return f"{self.id},{self.target_approval.name},erorr"        



class Clock(models.Model):
    CLOCK_TYPE= (
        ('1', '正常打卡'),
        ('2', '補打卡'),
    )
    employee_id = models.ForeignKey("Employee", related_name="clock",on_delete=models.CASCADE)
    type_of_clock = models.CharField(max_length=1, choices=CLOCK_TYPE, default="1", blank=True, null=True, verbose_name="打卡類別")
    clock_in_or_out = models.BooleanField(verbose_name="勾起來上班，沒勾下班")
    clock_date = models.DateField(default=timezone.now,verbose_name='打卡日期')
    clock_time = models.TimeField(null=True,blank=True,verbose_name='打卡時間')
    clock_GPS = models.CharField(null=True,blank=True,max_length=255)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "打卡紀錄"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['clock_date',"clock_time"]

    def __str__(self):
        return f"{self.employee_id}({self.type_of_clock})"

    @classmethod
    def get_hour_for_month(cls, user,year, month):#當月打卡
        day_clocks = cls.objects.filter(employee_id=user, clock_date__month=month,clock_date__year=year).order_by('clock_time')

        new_clock_records_id = []
        for record in day_clocks:
            if record.type_of_clock =="2":
                get_approval = record.clock_correction.all()[0].Approval
                if get_approval :
                    if get_approval.current_status =="completed":
                        new_clock_records_id.append(record.id)
            else:
                new_clock_records_id.append(record.id)
                

        day_clocks = cls.objects.filter(id__in = new_clock_records_id)

        first_day_of_month = datetime(year=year, month=month, day=1)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            last_day_of_month = first_day_of_month.replace(day=31)
        elif month == 2:
            y = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            if y :
                last_day_of_month = first_day_of_month.replace(day=29)
            else:
                last_day_of_month = first_day_of_month.replace(day=28)
        else:
            last_day_of_month = first_day_of_month.replace(day=30)

        month=[]
        #翹班時數
        miss_hours,miss_minutes =0,0

        for day in range((last_day_of_month - first_day_of_month).days + 1):

            date_to_check = (first_day_of_month + timedelta(days=day)).date()
            if date_to_check >= datetime.today().date():
                continue #不去計算當天跟之後

            date_to_check_string = (first_day_of_month + timedelta(days=day)).strftime('%Y/%m/%d')

            #判斷要上班嗎
            extra_work_day = None
            try:
                extra_work_day = ExtraWorkDay.objects.get(date=date_to_check)
                if extra_work_day.date_type == 'day_off':
                    continue
            except ExtraWorkDay.DoesNotExist:
                pass

            if date_to_check.weekday() >= 5 and extra_work_day ==None :  # 六日 且extra_work_day是None，有資料就是要上班    
                continue

            #今天需要上多久
            total_hour,total_minutes ,results = user.day_status(date_to_check) 
            over_time = timedelta(hours=total_hour, minutes=total_minutes)

            day_clock_records = day_clocks.filter(clock_date=date_to_check)
            day_clock_records_len= len(day_clock_records)

            if  total_hour==0 and total_minutes==0 : #整天請假
                month.append({"date":date_to_check_string,"status":"3","results":results})
                continue

            if day_clock_records_len==1: #只打一次卡
                month.append({"date":date_to_check_string,"status":"1","ear_time":day_clock_records})
                miss_hours+=8
            elif day_clock_records_len==0:# 沒打卡
                miss_hours+=8
                month.append({"date":date_to_check_string,"status":"0"})
            else:#計算早晚打卡時間
                ear_time = day_clock_records.earliest('clock_time').clock_time
                last_time =day_clock_records.latest('clock_time').clock_time
                ear_seconds = ear_time.hour * 3600 + ear_time.minute * 60 
                last_seconds = last_time.hour * 3600 + last_time.minute * 60 
                #上了多久小時
                time_difference = last_seconds - ear_seconds
              
                hours_worked = time_difference // 3600
                minutes_worked = (time_difference % 3600) // 60
                time_string = f"{hours_worked}時{minutes_worked}分"
                
                #有沒有滿足
                end_difference = over_time - timedelta(hours=hours_worked, minutes=minutes_worked)
                hours = end_difference.seconds // 3600
                minutes = (end_difference.seconds // 60) % 60            
                print(over_time,timedelta(hours=hours_worked, minutes=minutes_worked),end_difference,time_difference,time_string)

                
                if end_difference.total_seconds() <= 0:
                    pass
                    # if not pass_8_hoour:
                    #     month.append({"date":date_to_check_string,"status":"ok","ear_time":ear_time,"last_time":last_time,"results":results,"hours":time_string})
                else:
                    # print(hours,minutes,"曠職")
                    miss_string =f"(miss:{hours}時{minutes}分)"
                    miss_hours+=hours
                    miss_minutes += minutes
                    month.append({"date":date_to_check_string,"status":"no","ear_time":ear_time,"last_time":last_time,"hours":time_string,"miss":miss_string,"results":results})

        miss_hours += miss_minutes // 60 
        miss_minutes %= 60  
        return  {"list":month ,"miss_hours":miss_hours,"miss_minutes":miss_minutes}


# 部門
class Department(ModifiedModel):
    COMPANY_CHOICES = [
        ('艾力克電機', '艾力克電機'),
        ('維景', '維景'),
    ]

    belong_to_company =models.CharField(max_length=20,choices=COMPANY_CHOICES, null=True, blank=True,verbose_name="所屬公司")
    parent_department  = models.ForeignKey('self',max_length=30,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上層部門')
    department_name = models.CharField(max_length=30, null=True, blank=True,verbose_name='部門名稱')
    department_id = models.CharField(max_length=20, null=True, blank=True,verbose_name='部門編號')

    class Meta:
        verbose_name = "部門"   # 單數
        verbose_name_plural = verbose_name   #複數

    def __str__(self):
        return f"{self.department_name}({self.belong_to_company})"

# 工項管理
class Work_Item(ModifiedModel):
    item_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="品名規格")
    item_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="編號")
    unit = models.CharField(max_length=100, blank=True, null=True, verbose_name="單位")
    unit_price = models.IntegerField(blank=True, null=True, verbose_name="單價")
    created_by = models.ForeignKey("Employee",related_name="work_item_author", on_delete=models.SET_NULL, null=True, blank=True)

    def get_display_text(self):
        pn_id = f"工項-{str(self.id).zfill(5)}"
        return f"{pn_id} | {self.item_name} | {self.item_id} | {self.unit} | {self.unit_price}(價格)"

    def get_show_id(self):
        return f"工項-{str(self.id).zfill(5)}"


    class Meta:
        verbose_name = "工項資料庫"
        verbose_name_plural = verbose_name

#報價單
class Quotation(ModifiedModel):
    quotation_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='報價單編號')
    client = models.ForeignKey("Client",related_name="Quotation", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='客戶名稱')
    project_name = models.CharField(max_length=100, verbose_name="專案名稱",blank=True, null=True)
    tax_id = models.CharField(max_length=20, verbose_name="統一編號",blank=True, null=True)
    contact_person = models.CharField(max_length=50, verbose_name="聯絡人",blank=True, null=True)
    address = models.CharField(max_length=100,verbose_name="地址",blank=True, null=True)
    tel = models.CharField(max_length=20, verbose_name="電話",blank=True, null=True)
    mobile = models.CharField(max_length=20, verbose_name="手機",blank=True, null=True)
    fax = models.CharField(max_length=20, verbose_name="傳真",blank=True, null=True)
    email = models.EmailField(verbose_name="電子郵件",blank=True, null=True)
    quote_validity_period = models.IntegerField(verbose_name="報價單有效期",blank=True, null=True)
    business_tel = models.CharField(max_length=20, verbose_name="業務電話",blank=True, null=True)
    business_assistant = models.CharField(max_length=50, verbose_name="業務助理",blank=True, null=True)
    work_item = models.ManyToManyField(Work_Item,blank=True, related_name="quotations",verbose_name="工項")
    internal_content = models.TextField(blank=True, null=True, verbose_name='紀錄(對內)')
    created_by = models.ForeignKey("Employee",related_name="quotation_author", on_delete=models.SET_NULL, null=True, blank=True)
    invoice_attachment = models.FileField(upload_to="Invoice", null=True, blank=True, verbose_name="請款單")

    def get_show_id(self):
        return self.quotation_id


    # def __str__(self):
    #     return self.project_name

    class Meta:
        verbose_name = "報價單"
        verbose_name_plural = "報價單"

# 工程確認單
class Project_Confirmation(ModifiedModel):
    quotation =  models.ForeignKey("Quotation", null=True, blank=True,verbose_name="報價單號", on_delete=models.CASCADE )
    order_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='訂單編號')
    c_a = models.CharField(max_length=100, null=True, blank=True, verbose_name='母案編號')
    requisition = models.ForeignKey('Requisition', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='請購單位')
    turnover = models.CharField(max_length=10, null=True, blank=True, verbose_name='成交金額')
    is_completed = models.BooleanField(verbose_name='完工狀態',blank=True,default=False)
    completion_report_employee = models.ManyToManyField(Employee, related_name='projects_confirmation_report_employee', blank=True, verbose_name='完工回報人')
    completion_report_date = models.DateField(null=True, blank=True, verbose_name="完工回報日期")
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    attachment = models.FileField(upload_to="project_confirmation_reassignment_attachment", null=True, blank=True, verbose_name="完工重派附件")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='project_confirmation_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Confirmation_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')

    def get_show_id(self):
        return f"工確-{str(self.id).zfill(5)}"


    class Meta:
        verbose_name = "工程確認單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def __str__(self) :
        return   str(self.pk).zfill(5)

    def reassignment_attachment_link(self):
        if self.attachment:
            download_link = "<a href='{}' download>下載</a>".format(self.attachment.url)
            return mark_safe(download_link)
        else:
            return ""


# 工作派任計畫
class Project_Job_Assign(ModifiedModel):
    # 外鍵工程確認單，連帶帶出來的資料可重複（報價單號、工程名稱、客戶名稱）
    project_confirmation= models.ForeignKey(Project_Confirmation,on_delete=models.CASCADE,related_name='project',null=True, blank=True, verbose_name="工程確認單")
    attendance_date =models.DateField(null=True, blank=True, verbose_name="出勤日期")
    work_method = models.BooleanField(null=True, blank=True, verbose_name="工作方式(是:出勤、否:文書)",default=True) 
    work_employee = models.ManyToManyField('Employee', related_name='projects_work_employee', blank=True, verbose_name='工作人員')
    lead_employee = models.ManyToManyField('Employee', related_name='projects_lead_employee', blank=True, verbose_name="帶班人員")
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    location = models.CharField(max_length=4,choices=LOCATION_CHOICES, null=True, blank=True, verbose_name="工作地點")
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Project_Job_Assign_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Job_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')


    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def get_show_id(self):
        return f"派任-{str(self.id).zfill(5)}"



    @classmethod
    def get_month_list_day(cls, employee,year,month):#公派當月天數
        from collections import defaultdict

        employee_location = employee.location_city
        if employee_location =="":
            return {"error":f"{employee.full_name} 沒有選擇居住城市，無法計算"}

        conditions = Q(work_employee=employee) | Q(lead_employee=employee)
        assignments = cls.objects.filter(conditions, 
                                         attendance_date__year=year, 
                                         attendance_date__month=month).distinct()

        print(assignments)
        print(employee_location)

        allowance_dict = defaultdict(lambda: {"id":"","location": "", "day": 0, "money": 0,"food":0,"error":"","food_error":""})


        for assignment in assignments:
            location = assignment.location
            get_show_id = assignment.get_show_id()
            allowance_dict[get_show_id]["id"] = get_show_id

            if  location=="":
                allowance_dict[get_show_id]["error"] = "派任單未選擇城市"
                continue
                
            if assignment.work_method:  # 如果是出勤
                
                allowance_dict[get_show_id]["location"] = f"派工地-{location}"
                allowance_dict[get_show_id]["day"] += 1
                try:
                    get_Reference_obj = ReferenceTable.objects.get(name="出差津貼",
                                            location_city_residence=employee_location,
                                            location_city_business_trip=location)
                    allowance_dict[get_show_id]["money"] = get_Reference_obj.amount
                except ReferenceTable.DoesNotExist:
                    allowance_dict[get_show_id]["error"] = f"找不到{employee_location}對{location}的出差參照表 "
                try:
                    get_Reference_food_obj = ReferenceTable.objects.get(name="派工-伙食津貼",
                                            location_city_residence=employee_location,
                                            location_city_business_trip=location)
                    allowance_dict[get_show_id]["food"] = get_Reference_food_obj.amount
                except ReferenceTable.DoesNotExist:
                    allowance_dict[get_show_id]["food_error"] = f"找不到{employee_location}對{location}的伙食津貼參照表"
            else:
                allowance_dict[get_show_id]["location"] = f"非派工地-{location}"
                allowance_dict[get_show_id]["day"] += 1
                try:
                    get_Reference_food_obj = ReferenceTable.objects.get(name="非派工-伙食津貼",
                                            location_city_residence=employee_location,
                                            location_city_business_trip=location)
                    allowance_dict[get_show_id]["food"] = get_Reference_food_obj.amount
                except ReferenceTable.DoesNotExist:
                    allowance_dict[get_show_id]["food_error"] = f"找不到{employee_location}對{location}的伙食津貼參照表"

        allowance_list = [
            {
                "id": data["id"],
                "location": data["location"],
                "day": data["day"],
                "money": data.get("money",0),
                "food": data.get("food", 0),
                "error": data.get("error", ""),
                "food_error": data["food_error"],
            }
            for data in allowance_dict.values() if data["day"] >= 0
        ]
        total_money =  math.ceil(sum(data["money"] * data["day"] for data in allowance_list))
        total_food_money = math.ceil(sum(data["food"] * data["day"] for data in allowance_list))

        #回傳伙食津貼/出差津貼/明細
        return total_money,total_food_money, allowance_list
    
    def __str__(self) :
        return   str(self.pk).zfill(5)


# 派工單
class Project_Employee_Assign(ModifiedModel):
    # 外鍵工作派任計畫，連帶帶出來的資料可重複（報價單號、工程名稱、客戶名稱、請購單位，使用車輛?）
    project_job_assign= models.ForeignKey(Project_Job_Assign,on_delete=models.CASCADE,related_name='project_employee_assign',null=True, blank=True, verbose_name="工作派任計畫")
    construction_date = models.DateField(null=True, blank=True, verbose_name="施工日期")
    completion_date = models.DateField(null=True, blank=True, verbose_name="完工日期")
    is_completed = models.BooleanField(verbose_name='完工狀態',blank=True,default=False)
    inspector = models.ManyToManyField('Employee', related_name='employee_assign_work_employee', blank=True, verbose_name='檢測人員')
    manuscript_return_date = models.DateField(null=True, blank=True, verbose_name="手稿預計回傳日")
    lead_employee = models.ManyToManyField('Employee', related_name='employee_assign_lead_employee', blank=True, verbose_name='帶班主管')
    enterprise_signature = models.ImageField(upload_to="Employee_Assign_Signature",null=True, blank=True, verbose_name='業主簽名')
    carry_equipments = models.ManyToManyField('Equipment', related_name='carry_project', blank=True, verbose_name='攜帶資產')
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Project_Employee_Assign_Approval')
    test_description = models.TextField( verbose_name="檢查項目描述",null="",blank=True)
    test_items = models.TextField( verbose_name="檢查項目",null="",blank=True)
    remark = models.TextField( verbose_name="交接/備註",null="",blank=True)
    created_by = models.ForeignKey("Employee",related_name="Project_Employee_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')

    def enterprise_signature_link(self):
        if self.enterprise_signature:
            download_link = "<a href='{}' download>下載</a>".format(self.enterprise_signature.url)
            return mark_safe(download_link)
        else:
            return ""

    def test_items_split(self):
        return self.test_items.split(",")
    def get_show_id(self):
        return f"派工-{str(self.id).zfill(5)}"

    class Meta:
        verbose_name = "派工單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id'] 

    def __str__(self):
        return self.get_show_id()


class ExtraWorkDay(ModifiedModel):
    DATE_TYPE_CHOICES = [
        ('extra_work', '補班、額外上班日(這天要上班)'),
        ('day_off', '國定假日、平日休假日(這天不用上班)'),
    ]

    date = models.DateField(verbose_name="調整日期")
    date_type = models.CharField(max_length=10, choices=DATE_TYPE_CHOICES, verbose_name="日期類型")
    created_by = models.ForeignKey("Employee",related_name="ExtraWorkDay_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')

    class Meta:
        verbose_name = "工作日調整"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def get_show_id(self):
        return f"調假-{str(self.id).zfill(5)}"


    def __str__(self):
        return f"{self.date} - {self.get_date_type_display()}"

#車程津貼
class Travel_Application(ModifiedModel):
    date = models.DateField(verbose_name="申請日期",blank=True, null=True) 
    location_city_go = models.CharField(max_length=4,blank=True, null=True,default="", choices=LOCATION_CHOICES, verbose_name="出發地")
    location_city_end = models.CharField(max_length=4,blank=True, null=True,default="", choices=LOCATION_CHOICES, verbose_name="到達")
    attachment = models.FileField(upload_to="Travel_Application_Attachment", null=True, blank=True, verbose_name="車程津貼附件")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Travel_Application_Approval')
    created_by = models.ForeignKey("Employee",related_name="Travel_Application_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='申請者')

    class Meta:
        verbose_name = "車程申請"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def get_show_id(self):
        return f"車程-{str(self.id).zfill(5)}"

    def get_hour(self):        
        try:
            reference_entry = ReferenceTable.objects.get(
                location_city_business_trip=self.location_city_go,
                location_city_residence=self.location_city_end,
                name="車程津貼"
            )
            return True,reference_entry.amount
        except ReferenceTable.DoesNotExist:
            return False,f"找不到{self.location_city_go}對{self.location_city_end}的出差參照表 "

    @classmethod
    def get_time_cost_details_by_YM(cls, user, year, month):
        total_amount = 0
        get_hour_salary =user.get_hour_salary()
        details = []

        travel_apps = cls.objects.filter(
            created_by=user,
            date__year=year,
            date__month=month,
            Approval__current_status="completed"
        )

        for app in travel_apps:
            status, detail = app.get_hour()
            details.append({
                'id': app.get_show_id(),
                'detail': detail,
                'date':app.date,
                'location_city_go':app.location_city_go,
                'location_city_end':app.location_city_end,
            })

            if status:
                total_amount += detail
        if total_amount >17:
            total_amount =total_amount  - 16
            return total_amount ,math.ceil(total_amount*get_hour_salary*1.34), details
        else:
            return 0,0, details



# 請假申請
class Leave_Application(ModifiedModel):
    type_of_leave = models.ForeignKey("Leave_Param", on_delete=models.SET_NULL,related_name="lication", blank=True, null=True, verbose_name="假別項目")
    start_date_of_leave = models.DateField(blank=True, null=True, verbose_name="請假起始日期")
    end_date_of_leave = models.DateField(blank=True, null=True, verbose_name="請假結束日期")
    start_hours_of_leave = models.IntegerField(default=0,blank=True, null=True, verbose_name="請假起始小時")
    start_mins_of_leave = models.IntegerField(default=0,blank=True, null=True, verbose_name="請假起始分鐘")
    end_hours_of_leave = models.IntegerField(default=0,blank=True, null=True, verbose_name="請假結束小時")
    end_mins_of_leave = models.IntegerField(default=0,blank=True, null=True, verbose_name="請假結束分鐘")
    leave_hours = models.IntegerField(default=0, blank=True, null=True, verbose_name="申請時數(時)")
    leave_mins = models.IntegerField(default=0, blank=True, null=True, verbose_name="申請時數(分)")
    substitute = models.ForeignKey("Employee", on_delete=models.SET_NULL,related_name="leave_application_substitute", blank=True, null=True, verbose_name="工作代理人")
    leave_reason = models.TextField(max_length=300, blank=True, null=True, verbose_name="請假事由")
    backlog = models.CharField(max_length=100, blank=True, null=True, verbose_name="待辦事項")
    attachment = models.FileField(upload_to="Leave_Application_attachment", null=True, blank=True, verbose_name="請假附件")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Leave_Application_Approval')
    created_by = models.ForeignKey("Employee",related_name="leave_list", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='申請人')


    class Meta:
        verbose_name = "請假申請"
        verbose_name_plural = verbose_name

    def get_show_id(self):
        return f"假單-{str(self.id).zfill(5)}"

    def __str__(self):
        return self.get_show_id()
    
    def hour_day(self,day):#回傳這天請了多久，並附上詳細資訊
        total_days =  int((self.end_date_of_leave - self.start_date_of_leave).days)

        if total_days == 0: #只請一天
            leave_duration = timedelta(hours=self.end_hours_of_leave - self.start_hours_of_leave, 
                                                minutes=self.end_mins_of_leave - self.start_mins_of_leave)
            total_hours = leave_duration.seconds // 3600
            total_minutes = (leave_duration.seconds // 60) % 60
            if total_minutes < 30:
                total_minutes = 0
            else:
                total_minutes = 30

            if self.start_hours_of_leave < 13 and self.end_hours_of_leave >= 13 :
                total_hours -= 1
            return {"total_hours": total_hours, "total_minutes": total_minutes, "type_of_leave": self.type_of_leave.leave_name,"id":self.get_show_id()}

        else: #判斷day
            if self.start_date_of_leave == day:
                start_time = timedelta(hours=self.start_hours_of_leave, minutes=self.start_mins_of_leave)
                start_difference = timedelta(hours=17)- start_time 
                total_hours = start_difference.seconds // 3600
                total_minutes = (start_difference.seconds // 60) % 60
                if self.start_hours_of_leave < 13: #第一天是否在13點前請假
                    total_hours -= 1
                return {"total_hours": total_hours, "total_minutes": total_minutes, "type_of_leave": self.type_of_leave.leave_name,"id":self.get_show_id()}
            elif self.end_date_of_leave == day:
                end_time = timedelta(hours=self.end_hours_of_leave, minutes=self.end_mins_of_leave)
                end_difference = end_time - timedelta(hours=8)
                total_hours = end_difference.seconds // 3600
                total_minutes = (end_difference.seconds // 60) % 60
                if self.end_hours_of_leave >= 13:  # 最後天是否請超過下午
                        total_hours -= 1
                return {"total_hours": total_hours, "total_minutes": total_minutes, "type_of_leave": self.type_of_leave.leave_name,"id":self.get_show_id()}
            else: #請假整天
                return {"total_hours": 8, "total_minutes": 0,"type_of_leave": self.type_of_leave.leave_name,"id":self.get_show_id()}

    def calculate_leave_duration(self): #回傳這筆Leave_Application 請了多久小時 分鐘
        total_days =  int((self.end_date_of_leave - self.start_date_of_leave).days)

        if total_days==0:  # 請假只有一天
            leave_duration = timedelta(hours=self.end_hours_of_leave - self.start_hours_of_leave, 
                                                minutes=self.end_mins_of_leave - self.start_mins_of_leave)
            total_hours = leave_duration.seconds // 3600
            total_minutes = (leave_duration.seconds // 60) % 60
            if total_minutes < 30:
                total_minutes = 0
            else:
                total_minutes = 30

            if self.start_hours_of_leave < 13 and self.end_hours_of_leave >= 13 :
                total_hours -= 1

        else:

            #計算第一天上多久跟最後一天請多久。
            start_time = timedelta(hours=self.start_hours_of_leave, minutes=self.start_mins_of_leave)
            start_difference = timedelta(hours=17)- start_time 
            end_time = timedelta(hours=self.end_hours_of_leave, minutes=self.end_mins_of_leave)
            end_difference = end_time - timedelta(hours=8)
            total_difference = start_difference + end_difference
            total_hours = total_difference.seconds // 3600
            total_minutes = (total_difference.seconds // 60) % 60

            if self.start_hours_of_leave < 13: #第一天是否在13點前請假
                total_hours -= 1

            if self.end_hours_of_leave >= 13:  # 最後天是否請超過下午
                total_hours -= 1
            if total_minutes < 30:
                total_minutes = 0
            else:
                total_minutes = 30

            sleep_day =  total_days-2
            if sleep_day > 0:
                total_hours +=sleep_day *8


        return total_hours, total_minutes

    

class Leave_Param(ModifiedModel):
    GENDER_TYPE = (
        ('不限', '不限'),
        ('男', '男'),
        ('女', '女'),
    )
    UNIT_TYPE = (
        ('小時', '小時'),
        ('天', '天'),
    )
    LEAVE_TYPE = (
        ('特休假', '特休假'),
        ('補休假', '補休假'),
        ('一般假', '一般假'),
        ('特別假', '特別假'),
    )
    # leave_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="假別代碼")
    leave_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="假別名稱")
    leave_type = models.CharField(max_length=5, choices=LEAVE_TYPE,blank=True, null=True, verbose_name="項目類別")
    leave_quantity = models.IntegerField(blank=True, null=True, default=0, verbose_name="給假數(小時)")
    minimum_leave_number = models.DecimalField(max_digits=5, decimal_places=3,default=0, blank=True, null=True, verbose_name="最低請假數(為0就不卡控)")
    minimum_leave_unit = models.DecimalField(max_digits=5, decimal_places=3,default=0, blank=True, null=True, verbose_name="最小請假單位(為0就不卡控)")
    unit = models.CharField(max_length=5, choices=UNIT_TYPE,blank=True, null=True,verbose_name="單位")
    is_audit = models.BooleanField(blank=True, default=False, verbose_name="附件稽核")
    is_attachment = models.BooleanField(blank=True, default=False, verbose_name="附件提示")
    deduct_percentage = models.IntegerField(blank=True, null=True, default=0, verbose_name="扣薪 %")
    control = models.BooleanField(blank=True, default=True, verbose_name="假控")
    gender = models.CharField(max_length=5, choices=GENDER_TYPE,blank=True, null=True,verbose_name="性別")
    leave_rules = models.TextField(max_length=1000, blank=True, null=True, verbose_name="請假規定")
    created_by = models.ForeignKey("Employee",verbose_name="申請人",related_name="leave_param_author", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "假別參數"
        verbose_name_plural = verbose_name
    def get_show_id(self):
        return f"{str(self.id).zfill(5)}"

    def __str__(self):
        return self.leave_name

    #統一回傳leave_quantity，主要處理特休計算 才建立這個fuc
    def leave_hours(self,user):
        if self.id ==1: #特休id是1        
            start_work_date = user.start_work_date #入職日
            today = datetime.today()
            return 0

        return self.leave_quantity
    

    #根據YMD與user、核准狀況的參數 回傳Leave_Application arrays
    def get_user_leave_applications_by_YM_or_Total(self, user,Approval_status=None,year=None,month=None):
        applications = self.lication.filter(created_by=user)        
        if year:
            applications = applications.annotate(year=ExtractYear('start_date_of_leave')).filter(year=year)
        if month:
            applications = applications.annotate(month=ExtractMonth('start_date_of_leave')).filter(month=month)

        if Approval_status:
            applications = applications.filter(Approval__current_status="completed")
        return applications

    

    #傳入YM，計算範圍內的Leave_Application使用幾小時
    def calculate_leave_duration_by_YM_or_Total(self, user,Approval_status=None,year=None,month=None):
        total_hours = 0
        total_minutes = 0
        details =[]
        
        user_leave_applications = self.get_user_leave_applications_by_YM_or_Total(user=user,Approval_status=Approval_status,year=year,month=month)
        
        for leave_application in user_leave_applications:
            leave_hours, leave_minutes = leave_application.calculate_leave_duration()
            details.append({
                "id":leave_application.get_show_id(),
                "time":f"{leave_hours} : {leave_minutes}",
            })

            total_hours += leave_hours
            total_minutes += leave_minutes

        #進位
        total_hours += total_minutes // 60
        total_minutes %= 60

        return total_hours, total_minutes,details

    #計算核准通過的請假扣款，根據傳入YM
    def calculate_leave_cost_by_YM_or_Total(self, user,year,month):
        hourly_salary =user.get_hour_salary()
        #回傳已請假(簽核)
        total_hours, total_minutes ,_= self.calculate_leave_duration_by_YM_or_Total(user=user, Approval_status= True,year=year,month=month)
        total_cost = (total_hours * hourly_salary) + (total_minutes * hourly_salary / 2)
        #百分比
        deduction_percentage = self.deduct_percentage / 100
        total_cost *= deduction_percentage 
        return math.ceil(total_cost),total_hours,total_minutes
    

    #傳入新申請obj，判斷今年能不能請假
    def exceeds_leave_quantity_by_year(self, leave_application,user):
        year = leave_application.start_date_of_leave.year
        #取得今年請假時數
        total_hours, total_minutes ,_= self.calculate_leave_duration_by_YM_or_Total(user,year=year)        
        total_hours += total_minutes / 60
        #取得傳入的請假obj 使用多少小時
        leave_application_hours, leave_application_minutes = leave_application.calculate_leave_duration()
        #將已經請過的假 + 將要請的時數加在一起
        total_hours += leave_application_hours + leave_application_minutes / 60
        #判斷最低單位正常
        # pass_hours ,pass_minutes = self.minimum_leave_number*24 ,self.minimum_leave_unit*60

           
        #判斷累積時數是否超過
        return  self.leave_hours(user) > total_hours


    @classmethod #撈全部請假參數，範圍YM，每個參數請了多久小時，回傳已經使用多久小時的參數list
    def get_year_total_cost_list(cls, user,year,month):
        leave_param_details = []
        leave_params = cls.objects.all()

        for leave_param in leave_params:
            cost,total_hours, total_minutes  = leave_param.calculate_leave_cost_by_YM_or_Total(user=user,year=year,month=month)
            get_leave_param_hour = leave_param.leave_hours(user)

            if cost!=0:
                leave_param_details.append({
                    'id': leave_param.id,
                    'name': leave_param.leave_name,
                    'cost': cost,
                    'total_hours': total_hours,
                    'total_minutes': total_minutes,
                    'get_leave_param_hour': get_leave_param_hour,
                })

        return leave_param_details

    @classmethod #取得已經使用多久的假別的list
    def get_leave_param_all_details(cls, user,year=None,month=None):
        leave_param_details = []

        leave_params = cls.objects.all()#取得請假參數

        for leave_param in leave_params:#根據請假參數撈取 user請了多久小時
            total_hours, total_minutes , details = leave_param.calculate_leave_duration_by_YM_or_Total(user=user,year=year,month=month)
            can_use_hour = leave_param.leave_hours(user)

            remaining_hours = can_use_hour - total_hours
            remaining_minutes = 0  
            if total_minutes > 0:
                remaining_hours -= 1
                remaining_minutes = 60 - total_minutes

            leave_param_details.append({
                'id': leave_param.id,
                'name': leave_param.leave_name,
                'total_hours': total_hours,
                'total_minutes': total_minutes,
                'all_hour': can_use_hour,
                'remaining_time': f"{remaining_hours}時{remaining_minutes}分",
            })

        return leave_param_details

# 加班申請
class Work_Overtime_Application(ModifiedModel):
    SHIFT_TYPE= (
        ('1', '班前加班'),
        ('2', '班後加班'),
    )
    OVERTIME_TYPE= (
        ('1', '平日加班'),
    )
    CARRY_OVER_TYPE= (
        ('1', '加班費'),
    )
    date_of_overtime = models.DateField(blank=True, null=True, verbose_name="加班日期")
    shift_of_overtime = models.CharField(max_length=1, choices=SHIFT_TYPE, default="1", blank=False, null=False, verbose_name="班前/班後")
    type_of_overtime = models.CharField(max_length=1, choices=OVERTIME_TYPE, default="1", blank=False, null=False, verbose_name="加班類別")
    start_hours_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班起始小時")
    start_mins_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班起始分鐘")
    end_hours_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班結束小時")
    end_mins_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班結束分鐘")
    overtime_hours = models.IntegerField(default=0,blank=True, null=True, verbose_name="申請時數(時)")
    overtime_mins = models.IntegerField(default=0,blank=True, null=True, verbose_name="申請時數(分)")
    carry_over = models.CharField(max_length=100, choices=CARRY_OVER_TYPE, default="1", blank=False, null=False, verbose_name="加班結轉方式")
    overtime_reason = models.TextField(max_length=300, blank=True, null=True, verbose_name="加班事由")
    attachment = models.FileField(upload_to="Work_Overtime_Application_Attachment", null=True, blank=True, verbose_name="加班附件")
    created_by = models.ForeignKey("Employee",verbose_name="申請人",related_name="work_overtime_application_author", on_delete=models.SET_NULL, null=True, blank=True)
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Work_Overtime_Application_Approval')

    class Meta:
        verbose_name = "加班申請"
        verbose_name_plural = verbose_name


    def calculate_overtime_hours(self):

        start_time_minutes = self.start_hours_of_overtime * 60 + self.start_mins_of_overtime
        end_time_minutes = self.end_hours_of_overtime * 60 + self.end_mins_of_overtime

        overtime_minutes = end_time_minutes - start_time_minutes

        overtime_hours = overtime_minutes // 60
        overtime_minutes %= 60

        return overtime_hours, overtime_minutes

    @classmethod
    def get_money_by_user_month(cls, user, year, month):
            
        overtime_applications = cls.objects.filter(
            created_by=user,
            date_of_overtime__year=year,
            date_of_overtime__month=month,
            Approval__current_status="completed"
        )

        total_overtime_hours= 0
        details=[]
        for application in overtime_applications:
            overtime_hours, overtime_minutes = application.calculate_overtime_hours()
            add_hour=  overtime_hours + overtime_minutes / 60
            total_overtime_hours += add_hour
            details.append({"id":application.get_show_id(),"hour":add_hour})

        hourly_salary =user.get_hour_salary()
        total_overtime_money = math.ceil(total_overtime_hours * hourly_salary *1.34)

        return total_overtime_money,details



    def get_show_id(self):
        return f"加班-{str(self.id).zfill(5)}"

# 補卡申請
class Clock_Correction_Application(ModifiedModel):
    SHIFT_TYPE= (
        ('1', 'A班'),
    )
    CLOCK_CATEGORY= (
        ('1', '忘打卡'),
        ('2', '其他'),
    )
    CLOCK_TYPE= (
        ('1', '補上班'),
        ('2', '補下班'),
    )
    date_of_clock = models.DateField(blank=True, null=True, verbose_name="補卡日期")
    shift_of_clock = models.CharField(max_length=1, choices=SHIFT_TYPE, default="1", blank=False, null=False, verbose_name="補卡班別")
    category_of_clock = models.CharField(max_length=1, choices=CLOCK_CATEGORY, default="1", blank=False, null=False, verbose_name="補卡類別")
    type_of_clock = models.CharField(max_length=1, choices=CLOCK_TYPE, default="1", blank=False, null=False, verbose_name="補卡方式")
    end_hours_of_clock = models.IntegerField(default=0,blank=True, null=True, verbose_name="補卡小時")
    end_mins_of_clock = models.IntegerField(default=0,blank=True, null=True, verbose_name="補卡分鐘")
    clock_reason = models.TextField(max_length=300, blank=True, null=True, verbose_name="補卡事由")
    attachment = models.FileField(upload_to="Clock_Correction_Application_Attachment", null=True, blank=True, verbose_name="補卡附件")
    clock = models.ForeignKey("Clock",related_name="clock_correction", on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey("Employee",related_name="clock_correction_application_author", on_delete=models.SET_NULL, null=True, blank=True)
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Clock_Correction_Application_Approval')

    class Meta:
        verbose_name = "補卡申請"
        verbose_name_plural = verbose_name
    
    def get_show_id(self):
        return f"補卡-{str(self.id).zfill(5)}"
    
    def create_and_update_clock(self, employee, date_of_clock, clock_correction_application_type_of_clock, time):

        if clock_correction_application_type_of_clock == "1":
            true_or_false = True
        elif clock_correction_application_type_of_clock == "2":
            true_or_false = False
            
        if self.clock is None:
            print("Clock 建立")
            clock = Clock.objects.create(employee_id=employee, clock_date=date_of_clock, clock_in_or_out=true_or_false, type_of_clock="2", clock_time=time)
            self.clock = clock
            self.save()
        else:
            print("Clock 更新")
            self.clock.update(clock_date=date_of_clock, clock_in_or_out=true_or_false, clock_time=time)




# 固定資產管理
class Equipment(ModifiedModel):
    TRANSMITTER_SIZE = (
        ('1', '大'),
        ('2', '小'),
    )
    equipment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="資產標籤")
    order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="序號")
    equipment_category = models.CharField(max_length=100, blank=True, null=True, verbose_name="資產種類別")
    equipment_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="中類")
    equipment_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="品名")
    product_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="廠牌/型號")
    manufacturing_numbe = models.CharField(max_length=100, blank=True, null=True, verbose_name="製造序號")
    supplier = models.CharField(max_length=100, blank=True, null=True, verbose_name="供應商")
    invoice = models.CharField(max_length=100, blank=True, null=True, verbose_name="發票號碼")
    date_of_purchase = models.DateField(blank=True, null=True, verbose_name="購入日期")
    cost_including_tax = models.CharField(max_length=100,blank=True, null=True, verbose_name="購入成本(含稅)")
    buyer = models.CharField(max_length=100,blank=True, null=True, verbose_name="採購人")
    user = models.CharField(max_length=100,blank=True, null=True, verbose_name="使用人")
    custodian = models.CharField(max_length=100,blank=True, null=True, verbose_name="保管人")
    abnormal_condition = models.CharField(max_length=100,blank=True, null=True, verbose_name="異常狀態")
    abnormal_condition_description = models.CharField(max_length=100,blank=True, null=True, verbose_name="狀態說明")
    normal_or_abnormal = models.CharField(max_length=100,blank=True, null=True, verbose_name="正常/異常")
    abnormal_description = models.CharField(max_length=100,blank=True, null=True, verbose_name="異常說明")
    abnormal_img = models.ImageField(upload_to='equipment_abnormal_img/', blank=True, null=True, verbose_name="異常照片")
    buy_img = models.ImageField(upload_to='buy_img/', blank=True, null=True, verbose_name="買進照片")
    inventory = models.CharField(max_length=100, blank=True, null=True, verbose_name="盤點")
    produced_stickers = models.BooleanField(blank=True, default=True, verbose_name="需補產編貼紙")
    transmitter = models.CharField(max_length=1, choices=TRANSMITTER_SIZE, blank=True, null=True, verbose_name="發報器大小")
    storage_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="庫存地點")
    detailed_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="位置")
    warranty = models.CharField(max_length=100, blank=True, null=True, verbose_name="保固期")
    warranty_period = models.CharField(max_length=100, blank=True, null=True, verbose_name="保固期間")
    is_check = models.BooleanField(blank=True,default=True, verbose_name="校驗類別")
    latest_check_date = models.DateField(max_length=100, blank=True, null=True, verbose_name="最近一次校驗日")
    check_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="校驗報告編碼")
    check_remark = models.CharField(max_length=100, blank=True, null=True, verbose_name="校驗註記")
    maintenance_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修狀態")
    repair_date = models.DateField(blank=True, null=True, verbose_name="送修日")
    repair_finished_date = models.DateField(blank=True, null=True, verbose_name="完成日")
    number_of_repairs = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修累計次數")
    accruing_amounts = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修累計金額")

    class Meta:
        verbose_name = "固定資產管理"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        # return self.equipment_name or ''
        return self.equipment_name or "1"
        

# 車輛
class Vehicle(ModifiedModel):
    VEHICLE_TYPE = (
        ('R', '一般用車'),
        ('M', '經理配車'),
    )
    vehicle_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="車牌編號")
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPE, blank=True, null=True, verbose_name="車輛類型")

    class Meta:
        verbose_name = "車輛"
        verbose_name_plural = verbose_name
# 客戶
class Client(ModifiedModel):
    client_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="客戶簡稱")

    class Meta:
        verbose_name = "客戶簡稱"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.client_name  
    
# 請購單位
class Requisition(ModifiedModel):
    requisition_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="請購單位")

    class Meta:
        verbose_name = "請購單位"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.requisition_name  



# 公告
class News(ModifiedModel):
    NEWS_TYPE = (
        ('1', '獎懲規範'),
        ('2', '系統相關'),
        ('3', '出勤與薪資相關'),
        ('4', '車輛相關'),
        ('5', '津貼相關'),
        ('6', '異常報告相關'),
    )
    CATEGORY_TYPE = (
        ('1', '公告'),
        ('2', '文管'),
    )
    LEVEL_TYPE = (
        ('H', '高'),
        ('M', '中'),
        ('L', '低'),
    )
    title = models.CharField(max_length=30, blank=True, null=True, verbose_name="公告標題")
    category = models.CharField(max_length=1, choices=NEWS_TYPE, blank=True, null=True, verbose_name="公告類別")
    type = models.CharField(max_length=1, choices=CATEGORY_TYPE, blank=True, null=True, verbose_name="類別")
    level = models.CharField(max_length=1, choices=LEVEL_TYPE, blank=True, null=True, verbose_name="重要性")
    editor_content = models.TextField(blank=True, null=True, verbose_name='內容')
    attachment = models.FileField(upload_to="news_attachment", null=True, blank=True, verbose_name="公告附件")
    created_by = models.ForeignKey("Employee",related_name="New_author", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "最新消息"
        verbose_name_plural = verbose_name
    
    def save(self, *args, **kwargs):
        # Call the save method of the parent class (ModifiedModel) using super()
        super().save(*args, **kwargs)