from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
# 員工（以內建 User 擴增）
class Employee(models.Model):
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
    full_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='員工名稱')
    employee_id	 = models.CharField(max_length=30, blank=True,verbose_name='員工ID')
    # departments = models.ManyToManyField('Department', related_name='employees', blank=True, verbose_name='部門名稱')# 你可以通过department.employees.all()访问一个部门的所有员工。
    position = models.CharField(max_length=30, null=True, blank=True, verbose_name='職稱')
    phone_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='手機號碼')
    contact_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='聯絡電話')
    start_date = models.DateField(null=True, blank=True, verbose_name='到職日期')
    seniority = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='目前年資')
    id_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='身份證字號')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    age = models.IntegerField(null=True, blank=True, verbose_name='年齡')
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
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "員工"   # 單數
        verbose_name_plural = verbose_name   #複數

    # def __str__(self):
    #     return self.user.username


# 部門
class Department(models.Model):
    parent_department  = models.ForeignKey('self',max_length=30,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上層部門')
    department_name = models.CharField(max_length=30, null=True, blank=True,verbose_name='部門名稱')
    department_id = models.CharField(max_length=20, null=True, blank=True,verbose_name='部門編號')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "部門"   # 單數
        verbose_name_plural = verbose_name   #複數

    def __str__(self):
        if self.parent_department:
            return f"{self.department_name} ({self.parent_department.department_name})"
        return self.department_name

from django.utils.html import format_html
from django.utils.safestring import mark_safe

# 工程確認單
class Project_Confirmation(models.Model):
    quotation_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="報價單號")
    project_confirmation_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="工確單編號")
    project_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="工程名稱")
    order_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='訂單編號')
    c_a = models.CharField(max_length=100, null=True, blank=True, verbose_name='母案編號')
    client = models.CharField(max_length=100, null=True, blank=True, verbose_name='客戶簡稱')
    requisition = models.CharField(max_length=100, null=True, blank=True, verbose_name='請購單位')
    turnover = models.CharField(max_length=10, null=True, blank=True, verbose_name='成交金額') # 限制10個字輸入數字應該夠?
    is_completed = models.BooleanField(verbose_name='完工狀態')
    completion_report_employee = models.ForeignKey('Employee', related_name='projects_confirmation_report_employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='完工回報人')
    completion_report_date = models.DateField(null=True, blank=True, verbose_name="完工回報日期")
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    reassignment_attachment = models.FileField(upload_to="project_confirmation_reassignment_attachment", null=True, blank=True, verbose_name="完工重派附件")
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "工程確認單"   # 單數
        verbose_name_plural = verbose_name   #複數
    def __str__(self):
        return self.project_name
    def reassignment_attachment_link(self):
        if self.reassignment_attachment:
            download_link = "<a href='{}' download>下載</a>".format(self.reassignment_attachment.url)
            return mark_safe(download_link)
        else:
            return "無"

# 工作派任計畫
class Project_Job_Assign(models.Model):
    quotation_id = models.CharField(max_length=100,null=True, blank=True, verbose_name="報價單號")
    projecet_id = models.CharField(max_length=100,null=True, blank=True, verbose_name='工派單編號')
    project_name = models.CharField(max_length=100,null=True, blank=True, verbose_name="工程名稱") # 不做外鍵，透過quotation_id帶入
    c_a = models.CharField(max_length=100, null=True, blank=True, verbose_name='母案編號')
    attendance_date = models.DateField(null=True, blank=True, verbose_name="出勤日期")
    work_employee = models.ForeignKey('Employee', related_name='projects_work_employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='工作人員')
    lead_employee = models.ForeignKey('Employee', related_name='projects_lead_employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="帶班人員")
    vehicle = models.CharField(max_length=100,null=True, blank=True, verbose_name='使用車輛')
    location = models.CharField(max_length=100,null=True, blank=True, verbose_name="工作地點")
    project_type = models.CharField(max_length=100,null=True, blank=True, verbose_name='工作類型')
    remark = models.TextField(null=True, blank=True, verbose_name="備註")
    support = models.CharField(max_length=100,null=True, blank=True, verbose_name='支援人力')
    attachment = models.FileField(upload_to="project-attachment", null=True, blank=True, verbose_name="工確單附件")
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數

    def attachment_link(self):
        if self.attachment:
            return format_html("<a href='%s' download>下載</a>" % (self.attachment.url,))
        else:
            return "無"
    # 告訴admin這個包含HTML代碼，要幫忙解析
    attachment_link.allow_tags = True

# 公告
class News(models.Model):
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
    type = models.CharField(max_length=1, choices=NEWS_TYPE, blank=True, null=True, verbose_name="類別")
    level = models.CharField(max_length=1, choices=LEVEL_TYPE, blank=True, null=True, verbose_name="重要性")
    content = models.TextField(blank=True, null=True, verbose_name='內容')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "最新消息"   # 單數
        verbose_name_plural = verbose_name   #複數


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
        
