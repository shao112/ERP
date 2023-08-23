
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
from django.db.models import Q



class UploadedFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='employee_profile/users/')

    class Meta:
        verbose_name = '檔案上傳管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name



class ApprovalLog(models.Model):
    approval = models.ForeignKey("ApprovalModel", on_delete=models.DO_NOTHING, related_name='approval_logs')
    user = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, verbose_name='簽核者')
    content = models.TextField(blank=True, null=True, verbose_name='內容')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')

    class Meta:
        verbose_name = '簽核記錄'
        verbose_name_plural = '簽核記錄'



class Approval_TargetDepartment(models.Model):
    STATUS_CHOICES = [
        ('工程確認單', '工程確認單'),
        ('工程派任計畫單', '工程派任計畫單'),
        ('派工單', '派工單'),
    ]

    name =models.CharField(max_length=20,verbose_name="表單名稱",choices=STATUS_CHOICES)
    department_order = models.JSONField( blank=True, null=True,verbose_name="部門簽核順序")
    belong_department = models.ForeignKey('Department',related_name="belong_department", blank=True, null=True, on_delete=models.CASCADE,verbose_name="屬於哪部門的簽核")
    class Meta:
        verbose_name = '簽核流程管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name} - {self.belong_department}"



class ApprovalModel(models.Model):
    STATUS_CHOICES = [
        ('completed', '完成'),
        ('in_progress', '進行中'),
        ('rejected', '駁回'),
    ]

    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    #目前待簽
    current_department = models.ForeignKey('Department', verbose_name="待簽核",on_delete=models.CASCADE, related_name='current_approvals')
    target_department = models.ForeignKey(Approval_TargetDepartment,verbose_name="依附簽核", on_delete=models.CASCADE, related_name='approvals')


    def update_department_status(self, new_status):
        if new_status == 'approved':
            self.find_and_update_parent_department()
        else:
            self.current_status = new_status
            self.save()

    def find_and_update_parent_department(self):
        current_department = self.current_department
        target_department = self.target_department
        department_order = target_department.department_order
        
        #尋找簽核index
        current_index = department_order.index(current_department.id)
        #判斷是不是最後一個
        if current_index ==len(department_order)-1 :
            self.update_department_status("completed")
        else:
            next_department_id = department_order[current_index + 1]
            next_department = Department.objects.get(id=next_department_id)
            self.current_department = next_department
            self.save()

    def get_approval_log_list(self):
        """
        取得相關的 ApprovalLog 並整理成列表
        """
        print("modal log")
        get_approval_logs = self.approval_logs.all().order_by('id')  # 根據 ID 順序排序
        print(get_approval_logs)
        show_list = []
        
        for log in get_approval_logs: #處理簽過LOG
            show_list.append({
                "user_full_name": log.user.full_name,
                "department": log.user.departments.department_name,
                "department_pk": log.user.departments.pk,
                "content": log.content, 
                "status": "pass"
            })
        print(show_list)
        print("log end")


        current_department = self.current_department
        department_order = self.target_department.department_order  # 從 target_department 中獲取順序
        current_department_index = department_order.index(current_department.id)

        for department_id in department_order[current_department_index:]:
            department = Department.objects.get(id=department_id)
            if show_list:
                department_already_recorded = any(item["department_pk"] == department.pk for item in show_list)
            else:
                department_already_recorded = False

            if not department_already_recorded:
                show_list.append({
                    "user_full_name": None,
                    "user_department": None,
                    "content": None,
                    "department_pk": department.pk,
                    "status": "wait",
                    "department": department.department_name
                })

        return show_list

    class Meta:
        verbose_name = '簽核狀態'
        verbose_name_plural = verbose_name


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


class Clock(models.Model):
    employee_id = models.ForeignKey("Employee", related_name="clock",on_delete=models.CASCADE)
    clock_in_or_out = models.BooleanField()
    clock_time = models.TimeField()
    clock_GPS = models.CharField(max_length=255)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "打卡紀錄"   # 單數
        verbose_name_plural = verbose_name   #複數


# Create your models here.
# 員工（以內建 User 擴增）
# admin:admin IT0000:itadmin000
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


# 工程確認單
class Project_Confirmation(ModifiedModel):
    quotation_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="報價單號")
    project_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="工程名稱")
    order_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='訂單編號')
    c_a = models.CharField(max_length=100, null=True, blank=True, verbose_name='母案編號')
    client = models.CharField(max_length=100, null=True, blank=True, verbose_name='客戶簡稱')
    requisition = models.CharField(max_length=100, null=True, blank=True, verbose_name='請購單位')
    turnover = models.CharField(max_length=10, null=True, blank=True, verbose_name='成交金額')
    is_completed = models.BooleanField(verbose_name='完工狀態',blank=True,default=False)
    completion_report_employee = models.ManyToManyField(Employee, related_name='projects_confirmation_report_employee', blank=True, verbose_name='完工回報人')
    completion_report_date = models.DateField(null=True, blank=True, verbose_name="完工回報日期")
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    attachment = models.FileField(upload_to="project_confirmation_reassignment_attachment", null=True, blank=True, verbose_name="完工重派附件")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.CASCADE , related_name='project_confirmation_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Confirmation_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')


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
    #  = models.CharField(max_length=100,null=True, blank=True, verbose_name='工派單編號')
    attendance_date =models.DateField(null=True, blank=True, verbose_name="出勤日期")
    work_employee = models.ManyToManyField('Employee', related_name='projects_work_employee', blank=True, verbose_name='工作人員')
    lead_employee = models.ManyToManyField('Employee', related_name='projects_lead_employee', blank=True, verbose_name="帶班人員")
    # support_employee = models.ManyToManyField('Employee', related_name='projects_support_employee', blank=True,verbose_name='支援人力')
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    location = models.CharField(max_length=100,null=True, blank=True, verbose_name="工作地點")
    project_type = models.CharField(max_length=100,null=True, blank=True, verbose_name='工作類型')
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    # attachment = models.FileField(upload_to="project-attachment/", null=True, blank=True, verbose_name="工確單附件")
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.CASCADE , related_name='Project_Job_Assign_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Job_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')


    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']

    def __str__(self) :
        return   str(self.pk).zfill(5)

    # def attachment_link(self):
    #     if self.attachment:
    #         return format_html("<a href='%s' download>下載</a>" % (self.project_confirmation.attachment.url,))
    #     else:
    #         return ""
    # 告訴admin這個包含HTML代碼，要幫忙解析
    # attachment_link.allow_tags = True

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
    Approval =  models.ForeignKey(ApprovalModel, null=True, blank=True, on_delete=models.CASCADE , related_name='Project_Employee_Assign_Approval')
    created_by = models.ForeignKey("Employee",related_name="Project_Employee_Assign_author", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='建立人')


    class Meta:
        verbose_name = "派工單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']
    def __str__(self):
        return self.project_job_assign.job_assign_id


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

# 工項資料庫
class Work_Item(ModifiedModel):
    work_item_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="工項編號")
    item_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="品名規格")
    item_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="編號")
    unit = models.CharField(max_length=100, blank=True, null=True, verbose_name="單位")
    unit_price = models.IntegerField(blank=True, null=True, verbose_name="單價")

    class Meta:
        verbose_name = "工項資料庫"
        verbose_name_plural = verbose_name


class Quotation(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="客戶名稱")
    tax_id = models.CharField(max_length=20, verbose_name="統一編號")
    contact_person = models.CharField(max_length=50, verbose_name="聯絡人")
    address = models.TextField(verbose_name="地址")
    tel = models.CharField(max_length=20, verbose_name="電話")
    mobile = models.CharField(max_length=20, verbose_name="手機")
    fax = models.CharField(max_length=20, verbose_name="傳真")
    email = models.EmailField(verbose_name="電子郵件")
    project_name = models.CharField(max_length=100, verbose_name="專案名稱")
    quote_validity_period = models.IntegerField(verbose_name="報價單有效期")
    business_tel = models.CharField(max_length=20, verbose_name="業務電話")
    business_assistant = models.CharField(max_length=50, verbose_name="業務助理")
    work_item = models.ManyToManyField(Work_Item,blank=True,  related_name="quotations")


    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "報價單"
        verbose_name_plural = "報價單"


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
# 請購單位
class Requisition(ModifiedModel):
    requisition_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="請購單位")

    class Meta:
        verbose_name = "請購單位"
        verbose_name_plural = verbose_name



#處理自動建立簽核對象
@receiver(post_save, sender=Project_Job_Assign)
@receiver(post_save, sender=Project_Confirmation) 
@receiver(post_save, sender=Project_Employee_Assign) 
def create_approval(sender, instance, created, **kwargs):
    if created and not instance.Approval:
        user = get_current_authenticated_user()        
        user = user.employee
        get_department= user.departments #單一FK
        target_department = Approval_TargetDepartment.objects.filter(belong_department=get_department).first()
        if not target_department:
                    # 如果找不到對應的 Approval_TargetDepartment，可以採取適當的處理方式
                    return

        approval = ApprovalModel.objects.create(target_department=target_department,current_department=get_department)
        instance.Approval = approval
        instance.save()
