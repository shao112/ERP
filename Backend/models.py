from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
# 員工（以內建 User 擴增）
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id	 = models.CharField(max_length=30, blank=True,verbose_name='員工ID')
    departments = models.ManyToManyField('Department', related_name='employees', blank=True, verbose_name='部門')# 你可以通过department.employees.all()访问一个部门的所有员工。
    position = models.CharField(max_length=30, blank=True,verbose_name='職位')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.employee.save()
    except Employee.DoesNotExist:
        pass

# 部門
class Department(models.Model):
    parent_department  = models.ForeignKey('self',max_length=30,  on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上層部門')
    department_name = models.CharField(max_length=30, blank=True,verbose_name='部門名稱')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "部門"   # 單數
        verbose_name_plural = verbose_name   #複數

    def __str__(self):
        if self.parent_department:
            return f"{self.department_name} ({self.parent_department.department_name})"
        return self.department_name


# 工作派任計畫
class Project(models.Model):
    quotation_id = models.CharField(max_length=30, verbose_name="報價單號")
    projecet_id = models.CharField(max_length=30, verbose_name='工派單編號')
    project_name = models.CharField(max_length=30, verbose_name="工程名稱")
    c_a = models.CharField(max_length=50, verbose_name='母案編號')
    attendance_date = models.DateField(null=True, blank=True, verbose_name="出勤日期")
    work_employee = models.ForeignKey('Employee', related_name='projects_work_employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='工作人員')
    lead_employee = models.ForeignKey('Employee', related_name='projects_lead_employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="帶班人員")
    vehicle = models.CharField(max_length=30, verbose_name='使用車輛')
    location = models.CharField(max_length=30, verbose_name="工作地點")
    project_type = models.CharField(max_length=30, verbose_name='工作類型')
    remark = models.CharField(max_length=30, null=True, blank=True, verbose_name="備註")
    support = models.CharField(max_length=30, verbose_name='支援人力')
    attachment = models.FileField(upload_to="project-attachment", null=True, blank=True, verbose_name="工確單附件")
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "工作派任計畫"   # 單數
        verbose_name_plural = verbose_name   #複數

# 公告
class News(models.Model):
    News_type = (
        ('1', '財務部'),
        ('2', '員工相關'),
    )
    title = models.CharField(max_length=30, verbose_name="標題")
    type = models.CharField(max_length=1, choices=News_type)
    content = models.TextField(blank=True, null=True, verbose_name='編輯器內文')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "最新消息"   # 單數
        verbose_name_plural = verbose_name   #複數