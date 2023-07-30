
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user


class Approval(models.Model):
    finish = models.BooleanField(default=False, verbose_name='完成')
    class Meta:
        verbose_name = '簽核狀態'
        verbose_name_plural = '簽核狀態'
        permissions = ( ('can_approval', '簽核權限'), )
    def __str__(self):
        return f'Approval {self.id}'


class ApprovalLog(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.DO_NOTHING, related_name='approval_logs')
    user = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, verbose_name='簽核者')
    content = models.TextField(blank=True, null=True, verbose_name='內容')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')

    class Meta:
        verbose_name = '簽核記錄'
        verbose_name_plural = '簽核記錄'

    def __str__(self):
        return f'ApprovalLog {self.id}'


class ApprovalModel(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.DO_NOTHING, related_name='approval')

    class Meta:
        abstract = True



#紀錄修改者
class ModifiedModel(models.Model):
    modified_by = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        # print("xxx save")
        # Get the current authenticated user
        user = get_current_authenticated_user()
        self.modified_by = user.employee
        super().save(*args, **kwargs)

    def update_fields_and_save(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()


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
    full_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='員工名稱')
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

    # def __str__(self):
    #     return self.user.username


# 部門
class Department(ModifiedModel):
    parent_department  = models.ForeignKey('self',max_length=30,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上層部門')
    department_name = models.CharField(max_length=30, null=True, blank=True,verbose_name='部門名稱')
    department_id = models.CharField(max_length=20, null=True, blank=True,verbose_name='部門編號')

    class Meta:
        verbose_name = "部門"   # 單數
        verbose_name_plural = verbose_name   #複數

    def __str__(self):
        if self.parent_department:
            return f"{self.department_name} ({self.parent_department.department_name})"
        return self.department_name


# 工程確認單
class Project_Confirmation(ModifiedModel):
    project_confirmation_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="工確單編號")
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
    reassignment_attachment = models.FileField(upload_to="project_confirmation_reassignment_attachment", null=True, blank=True, verbose_name="完工重派附件")

    class Meta:
        verbose_name = "工程確認單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']
    # def __str__(self):
    #     return self.project_name
    
    def reassignment_attachment_link(self):
        if self.reassignment_attachment:
            download_link = "<a href='{}' download>下載</a>".format(self.reassignment_attachment.url)
            return mark_safe(download_link)
        else:
            return "無"


# 工作派任計畫
class Project_Job_Assign(ModifiedModel):
    project_confirmation= models.ForeignKey(Project_Confirmation,on_delete=models.DO_NOTHING,related_name='project',null=True, blank=True, verbose_name="工程確認單") # 連帶帶出來的資料可重複
    attendance_date =models.JSONField(null=True, blank=True, verbose_name="出勤日期")
    work_employee = models.ManyToManyField('Employee', related_name='projects_work_employee', blank=True, verbose_name='工作人員')
    lead_employee = models.ManyToManyField('Employee', related_name='projects_lead_employee', blank=True, verbose_name="帶班人員")
    # support_employee = models.ManyToManyField('Employee', related_name='projects_support_employee', blank=True,verbose_name='支援人力')
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    location = models.CharField(max_length=100,null=True, blank=True, verbose_name="工作地點")
    project_type = models.CharField(max_length=100,null=True, blank=True, verbose_name='工作類型')
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    attachment = models.FileField(upload_to="project-attachment/", null=True, blank=True, verbose_name="工確單附件")

    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']


    def attachment_link(self):
        if self.attachment:
            return format_html("<a href='%s' download>下載</a>" % (self.attachment.url,))
        else:
            return "無"
    # 告訴admin這個包含HTML代碼，要幫忙解析
    attachment_link.allow_tags = True

# 派工單
class Project_Employee_Assign(ModifiedModel):
    # 外鍵工程確認單，連帶帶出來的資料可重複（報價單號、工程名稱、客戶名稱、請購單位）
    project_confirmation= models.ForeignKey(Project_Confirmation,on_delete=models.DO_NOTHING,related_name='project_employee_assign',null=True, blank=True, verbose_name="工程確認單")
    construction_date = models.DateField(null=True, blank=True, verbose_name="施工日期")
    completion_date = models.DateField(null=True, blank=True, verbose_name="完工日期")
    is_completed = models.BooleanField(verbose_name='完工狀態',blank=True,default=False)
    construction_location = models.CharField(max_length=100,null=True, blank=True, verbose_name='施工地點')
    inspector = models.ManyToManyField('Employee', related_name='employee_assign_work_employee', blank=True, verbose_name='檢測人員')
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    manuscript_return_date = models.DateField(null=True, blank=True, verbose_name="手稿預計回傳日")
    lead_employee = models.ManyToManyField('Employee', related_name='employee_assign_lead_employee', blank=True, verbose_name='帶班主管')
    enterprise_signature = models.ImageField(null=True, blank=True, verbose_name='業主簽名')

    class Meta:
        verbose_name = "派工單"   # 單數
        verbose_name_plural = verbose_name   #複數
        ordering = ['-id']


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

    class Meta:
        verbose_name = "最新消息"   # 單數
        verbose_name_plural = verbose_name   #複數
    
    def save(self, *args, **kwargs):
        # Call the save method of the parent class (ModifiedModel) using super()
        super().save(*args, **kwargs)


class Clock(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in_or_out = models.BooleanField()
    clock_time = models.TimeField()
    clock_GPS = models.CharField(max_length=255)
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "打卡紀錄"   # 單數
        verbose_name_plural = verbose_name   #複數

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
    inventory = models.CharField(max_length=100, blank=True, null=True, verbose_name="盤點")
    produced_stickers = models.BooleanField(blank=True, null=True, verbose_name="需補產編貼紙")
    transmitter = models.CharField(max_length=1, choices=TRANSMITTER_SIZE, blank=True, null=True, verbose_name="發報器大小")
    storage_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="庫存地點")
    detailed_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="位置")
    warranty = models.CharField(max_length=100, blank=True, null=True, verbose_name="保固期")
    warranty_period = models.CharField(max_length=100, blank=True, null=True, verbose_name="保固期間")
    is_check = models.BooleanField(blank=True, null=True, verbose_name="校驗類別")
    latest_check_date = models.DateField(max_length=100, blank=True, null=True, verbose_name="最近一次校驗日")
    check_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="校驗報告編碼")
    check_remark = models.CharField(max_length=100, blank=True, null=True, verbose_name="校驗註記")
    maintenance_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修狀態")
    repair_date = models.DateField(blank=True, null=True, verbose_name="送修日")
    repair_finished_date = models.DateField(blank=True, null=True, verbose_name="完成日")
    number_of_repairs = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修累計次數")
    accruing_amounts = models.CharField(max_length=100, blank=True, null=True, verbose_name="維修累計金額")

    class Meta:
        verbose_name = "固定資產管理"   # 單數
        verbose_name_plural = verbose_name   #複數
        
