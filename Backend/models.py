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
    departments = models.ManyToManyField('Department', related_name='employees', blank=True, verbose_name='部門')
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
    department_id = models.CharField(max_length=30, blank=True,verbose_name='部門ID')
    department_name = models.CharField(max_length=30, blank=True,verbose_name='部門名稱')
    created_date = models.DateField(default=timezone.now,verbose_name='建立日期')
    update_date = models.DateField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = "部門"   # 單數
        verbose_name_plural = verbose_name   #複數

# 部門
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