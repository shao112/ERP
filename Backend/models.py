
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user
from datetime import date
import os
from django.db.models import F, Sum

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

#紀錄修改者
class ModifiedModel(models.Model):
    modified_by = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        user = get_current_authenticated_user()
        
        if user !=None:
            self.modified_by = user.employee            
            if hasattr(self, 'created_by'):
                if self.created_by ==None:
                    self.created_by =user.employee
 
        super().save(*args, **kwargs)

    def update_fields_and_save(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

class ReferenceTable(models.Model):
    location_city_residence = models.CharField(max_length=4, choices=LOCATION_CHOICES, verbose_name="居住地")
    location_city_business_trip = models.CharField(max_length=4, choices=LOCATION_CHOICES, verbose_name="出差地")
    amount = models.PositiveIntegerField(verbose_name="金額")
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
    location_city = models.CharField(max_length=4, choices=LOCATION_CHOICES, null=True, blank=True, verbose_name='居住城市(用於計算津貼)')
    uploaded_files = models.ManyToManyField(UploadedFile,blank=True,  related_name="userfile")
    full_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='員工名稱')
    employee_id	 = models.CharField(max_length=30, blank=True,verbose_name='員工ID')
    departments = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='employees', verbose_name='部門名稱')# 你可以通过department.employees.all()访问一个部门的所有员工。
    position = models.CharField(max_length=30, null=True, blank=True, verbose_name='職稱')
    phone_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='手機號碼')
    contact_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='聯絡電話')
    start_date = models.DateField(null=True, blank=True, verbose_name='到職日期')
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
    default_salary = models.IntegerField(default=27000, null=True, blank=True, verbose_name="薪資")#預設薪資

    class Meta:
        verbose_name = "員工"   # 單數
        verbose_name_plural = verbose_name   #複數

    # def employee_data_upload_path(instance, filename):
    #     employee_id = instance.id
    #     return os.path.join("Employee_data", str(employee_id), filename)


    def calSeniority(self):
        # current_date = date.today()
        # seniority = current_date.year - self.start_date.year
        # if (self.start_date.month, self.start_date.day) > (current_date.month, current_date.day):
        #     seniority -= 1
        # return round(seniority, 1)
        return 0

    def __str__(self):
        return self.full_name


class SalaryDetail(models.Model):
    salary = models.ForeignKey("Salary",related_name="details",on_delete=models.CASCADE, verbose_name="依附薪資單",null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='名稱')
    system_amount = models.PositiveIntegerField(default=0, verbose_name='系統金額')
    adjustment_amount = models.PositiveIntegerField(default=0, verbose_name='調整金額')
    deduction = models.BooleanField(default=False, verbose_name='扣款項目') #F為補貼、T為請事假、勞保...

    def set_name_and_adjustment_amount(self, name, amount,deduction):
        self.name = name
        self.deduction = deduction
        self.adjustment_amount = amount
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
        print(total_amount)
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
        ('Work_Overtime_Application', '補卡單'),
        ('Clock_Correction_Application', '加班單'),
    ]
    name =models.CharField(max_length=30,verbose_name="表單名稱",choices=STATUS_CHOICES)
    approval_order = models.JSONField(null=True, verbose_name="員工簽核順序")#儲存員工ID、各自主管(X)
    class Meta:
        verbose_name = '簽核流程管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_name_display()}"


class ApprovalModel(models.Model):
    STATUS_CHOICES = [
        ('completed', '完成'),
        ('in_progress', '進行中'),
        ('rejected', '駁回'),
    ]
    #related_name 關聯
    RELATED_NAME_MAP = {
        'Project_Confirmation': 'project_confirmation_Approval',
        'Project_Job_Assign': 'Project_Job_Assign_Approval',
        'Project_Employee_Assign': 'Project_Employee_Assign_Approval',
    }

    #對應的model，會帶入data-model
    Modal_URL__MAP = {
        'Project_Confirmation': 'project_confirmation',
        'Project_Job_Assign': 'job_assign',
        'Project_Employee_Assign': 'project_employee_assign',
    }


    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='in_progress')
    #目前待簽index
    current_index = models.IntegerField( verbose_name="待簽核index",default=0,blank=True,null=True)
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

            for employee_id in self.target_approval.approval_order:
                if employee_id == "x":
                    department_employees = self.get_created_by.departments.employees.all()
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
        related_name = self.RELATED_NAME_MAP.get(self.target_approval.name)
        if related_name:
            getobj = getattr(self, related_name, None).all()
            if len(getobj)!=0:
                return getattr(self, related_name, None).all()[0]
            return None
        return None
    


    def get_approval_employee(self):
        current_index= self.current_index
        approval_order = self.target_approval.approval_order
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
        approval_order = self.target_approval.approval_order
        
        #判斷是不是最後一個
        if current_index ==len(approval_order)-1 :
            self.update_department_status("completed")
        else:
            current_index+=1
            self.current_index = current_index
            self.save()

    def get_approval_log_list(self):
        """
        取得相關的 ApprovalLog 並整理成列表
        """
        get_approval_logs = self.approval_logs.all().order_by('id')  # 根據 ID 順序排序
        show_list = []
        current_index = self.current_index
        approval_order = self.target_approval.approval_order
        
        for index, log in enumerate(get_approval_logs): #處理簽過LOG
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

        return show_list

    class Meta:
        verbose_name = '簽核執行'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        get_foreignkey = self.get_foreignkey()
        get_show_id =""
        get_created_by =""
        if get_foreignkey !="":
            get_show_id = get_foreignkey.get_show_id()
            get_created_by =get_foreignkey.created_by
        
        return f"{self.target_approval.name} - {get_created_by} - {get_show_id}"
    


class Clock(models.Model):
    CLOCK_TYPE= (
        ('1', '正常打卡'),
        ('2', '補打卡'),
    )
    employee_id = models.ForeignKey("Employee", related_name="clock",on_delete=models.CASCADE)
    type_of_clock = models.CharField(max_length=1, choices=CLOCK_TYPE, default="1", blank=True, null=True, verbose_name="打卡類別")
    clock_in_or_out = models.BooleanField()
    clock_time = models.TimeField()
    clock_GPS = models.CharField(max_length=255)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "打卡紀錄"   # 單數
        verbose_name_plural = verbose_name   #複數
    def __str__(self):
        return f"{self.employee_id}({self.type_of_clock})"


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
        pn_id = f"WT-{str(self.id).zfill(5)}"
        return f"{pn_id} | {self.item_name} | {self.item_id} | {self.unit} | {self.unit_price}(價格)"

    def get_show_id(self):
        return f"工項-{str(self.id).zfill(5)}"


    class Meta:
        verbose_name = "工項資料庫"
        verbose_name_plural = verbose_name

#報價單
class Quotation(ModifiedModel):
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
        return f"報價-{str(self.id).zfill(5)}"


    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "報價單"
        verbose_name_plural = "報價單"

# 工程確認單
class Project_Confirmation(ModifiedModel):
    quotation =  models.ForeignKey("Quotation", null=True, blank=True,verbose_name="報價單號", on_delete=models.CASCADE )
    order_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='訂單編號')
    c_a = models.CharField(max_length=100, null=True, blank=True, verbose_name='母案編號')
    requisition = models.CharField(max_length=100, null=True, blank=True, verbose_name='請購單位')
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
    work_employee = models.ManyToManyField('Employee', related_name='projects_work_employee', blank=True, verbose_name='工作人員')
    lead_employee = models.ManyToManyField('Employee', related_name='projects_lead_employee', blank=True, verbose_name="帶班人員")
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    location = models.CharField(max_length=100,null=True, blank=True, verbose_name="工作地點")
    project_type = models.CharField(max_length=100,null=True, blank=True, verbose_name='工作類型')
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Project_Job_Assign_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Job_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')

    # def get_id():

    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def get_show_id(self):
        return f"工派-{str(self.id).zfill(5)}"


    def __str__(self) :
        return   str(self.pk).zfill(5)


# 派工單
class Project_Employee_Assign(ModifiedModel):
    # 外鍵工作派任計畫，連帶帶出來的資料可重複（報價單號、工程名稱、客戶名稱、請購單位，使用車輛?）
    project_job_assign= models.ForeignKey(Project_Job_Assign,on_delete=models.CASCADE,related_name='project_employee_assign',null=True, blank=True, verbose_name="工作派任計畫")
    construction_date = models.DateField(null=True, blank=True, verbose_name="施工日期")
    completion_date = models.DateField(null=True, blank=True, verbose_name="完工日期")
    is_completed = models.BooleanField(verbose_name='完工狀態',blank=True,default=False)
    construction_location = models.CharField(max_length=100,null=True, blank=True, verbose_name='施工地點')
    inspector = models.ManyToManyField('Employee', related_name='employee_assign_work_employee', blank=True, verbose_name='檢測人員')
    manuscript_return_date = models.DateField(null=True, blank=True, verbose_name="手稿預計回傳日")
    lead_employee = models.ManyToManyField('Employee', related_name='employee_assign_lead_employee', blank=True, verbose_name='帶班主管')
    enterprise_signature = models.ImageField(upload_to="Employee_Assign_Signature",null=True, blank=True, verbose_name='業主簽名')
    carry_equipments = models.ManyToManyField('Equipment', related_name='carry_project', blank=True, verbose_name='攜帶資產')
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Project_Employee_Assign_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Employee_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')


    def get_show_id(self):
        return f"派工-{str(self.id).zfill(5)}"


    class Meta:
        verbose_name = "派工單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']
    def __str__(self):
        return self.get_show_id()


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


# 請假申請
class Leave_Application(ModifiedModel):
    type_of_leave = models.ForeignKey("Leave_Param", on_delete=models.SET_NULL,related_name="leave_param", blank=True, null=True, verbose_name="假別項目")
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
    created_by = models.ForeignKey("Employee",related_name="leave_author", on_delete=models.SET_NULL, null=True, blank=True)
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Leave_Application_Approval')

    class Meta:
        verbose_name = "請假申請"
        verbose_name_plural = verbose_name
    # def cal_leave_hours(self):
    #     self.leave_hours = self.end_hours_of_leave - self.start_hours_of_leave
    #     return self.leave_hours
    # def cal_leave_mins(self):
    #     self.leave_mins = self.end_mins_of_leave - self.start_mins_of_leave
    #     return self.leave_mins
    # def get_leave_hours(self):
    #     return f"{str(self.cal_leave_hours()).zfill(2)}"
    # def get_leave_mins(self):
    #     return f"{str(self.cal_leave_mins()).zfill(2)}"
    
# 假別參數
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
    leave_quantity = models.IntegerField(blank=True, null=True, default=0, verbose_name="給假數")
    minimum_leave_number = models.DecimalField(max_digits=5, decimal_places=3,default=0, blank=True, null=True, verbose_name="最低請假數(為0就不卡控)")
    minimum_leave_unit = models.DecimalField(max_digits=5, decimal_places=3,default=0, blank=True, null=True, verbose_name="最小請假單位(為0就不卡控)")
    unit = models.CharField(max_length=5, choices=UNIT_TYPE,blank=True, null=True,verbose_name="單位")
    is_audit = models.BooleanField(blank=True, default=False, verbose_name="附件稽核")
    is_attachment = models.BooleanField(blank=True, default=False, verbose_name="附件提示")
    deduct_percentage = models.IntegerField(blank=True, null=True, default=0, verbose_name="扣薪 %")
    control = models.BooleanField(blank=True, default=True, verbose_name="假控")
    gender = models.CharField(max_length=5, choices=GENDER_TYPE,blank=True, null=True,verbose_name="性別")
    leave_rules = models.TextField(max_length=1000, blank=True, null=True, verbose_name="請假規定")
    created_by = models.ForeignKey("Employee",related_name="leave_param_author", on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "假別參數"
        verbose_name_plural = verbose_name
    def get_show_id(self):
        return f"{str(self.id).zfill(5)}"
    def __str__(self):
        return self.leave_name

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
    shift_of_overtime = models.CharField(max_length=1, choices=SHIFT_TYPE, blank=True, null=True, verbose_name="班前/班後")
    type_of_overtime = models.CharField(max_length=1, choices=OVERTIME_TYPE, blank=True, null=True, verbose_name="加班類別")
    start_hours_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班起始小時")
    start_mins_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班起始分鐘")
    end_hours_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班結束小時")
    end_mins_of_overtime = models.IntegerField(default=0,blank=True, null=True, verbose_name="加班結束分鐘")
    overtime_hours = models.IntegerField(default=0,blank=True, null=True, verbose_name="申請時數(時)")
    overtime_mins = models.IntegerField(default=0,blank=True, null=True, verbose_name="申請時數(分)")
    carry_over = models.CharField(max_length=100, choices=CARRY_OVER_TYPE, blank=True, null=True, verbose_name="加班結轉方式")
    overtime_reason = models.TextField(max_length=300, blank=True, null=True, verbose_name="加班事由")
    created_by = models.ForeignKey("Employee",related_name="work_overtime_application_author", on_delete=models.SET_NULL, null=True, blank=True)
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Work_Overtime_Application_Approval')

    class Meta:
        verbose_name = "加班申請"
        verbose_name_plural = verbose_name

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
    shift_of_clock = models.CharField(max_length=1, choices=SHIFT_TYPE, blank=True, null=True, verbose_name="補卡班別")
    category_of_clock = models.CharField(max_length=1, choices=CLOCK_CATEGORY, blank=True, null=True, verbose_name="補卡類別")
    type_of_clock = models.CharField(max_length=1, choices=CLOCK_TYPE, blank=True, null=True, verbose_name="補卡方式")
    end_hours_of_clock = models.IntegerField(default=0,blank=True, null=True, verbose_name="補卡小時")
    end_mins_of_clock = models.IntegerField(default=0,blank=True, null=True, verbose_name="補卡分鐘")
    clock_reason = models.TextField(max_length=300, blank=True, null=True, verbose_name="補卡事由")
    clock = models.ForeignKey("Clock",related_name="clock_correction_application", on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey("Employee",related_name="clock_correction_application_author", on_delete=models.SET_NULL, null=True, blank=True)
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.SET_NULL , related_name='Clock_Correction_Application_Approval')

    class Meta:
        verbose_name = "補卡申請"
        verbose_name_plural = verbose_name


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
        return self.equipment_name  
        

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



# #處理自動建立簽核對象
# @receiver(post_save, sender=Project_Job_Assign)
# @receiver(post_save, sender=Project_Confirmation) 
# @receiver(post_save, sender=Project_Employee_Assign) 
# def create_approval(sender, instance, created, **kwargs):
#     if created and not instance.Approval:
#         user = get_current_authenticated_user()        
#         user = user.employee
#         get_department= user.departments #單一FK
#         target_department = Approval_TargetDepartment.objects.filter(belong_department=get_department).first()
#         if not target_department:
            
#                     # 如果找不到對應的 Approval_TargetDepartment，可以採取適當的處理方式
#                     return

#         approval = ApprovalModel.objects.create(target_department=target_department,current_department=get_department)
#         instance.Approval = approval
#         instance.save()
