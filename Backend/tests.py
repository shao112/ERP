from django.test import TestCase, RequestFactory,TransactionTestCase
from django.urls import reverse
from django.http import JsonResponse
from .views import Project_Confirmation_View
from .models import Project_Confirmation, Project_Job_Assign, Project_Employee_Assign,Employee

from django.contrib.auth.models import User
from . import views
from .views import Project_Confirmation_View, Job_Assign_View, Project_Employee_Assign_View


class EmployeeModelTest(TransactionTestCase):
    def test_create_user_and_employee(self):
        # 创建 User 对象
        user = User.objects.create_user(username='your_username', password='your_password')

        # 创建 Employee 对象
        employee = Employee.objects.create(
            user=user,
            full_name='單元測試員工',
            employee_id='BXXX1323',
            # 其他字段...
        )

        # 验证是否成功创建 User 和 Employee 对象
        self.assertIsNotNone(user)
        self.assertIsNotNone(employee)

        # 验证 User 和 Employee 关联是否正确
        self.assertEqual(employee.user, user)



class EmployeeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.employee_1 = Employee.objects.create(
                    user=None,  # 设置 user 为 None
                    full_name='Employee 1',
                    employee_id='EMP001',
                    # 其他字段...
                )

        
    def test_get_employee(self):
        # 构造 GET 请求
        url = reverse('project_employee_api')
        request = self.factory.get(url, {'id': self.employee_1.id})

        # 调用视图函数
        response = views.Employee_View.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # 断言返回的 JSON 数据是否正确
        # expected_data = {
        #     # 预期的数据，根据您的记录内容进行修改
        # }
        # self.assertJSONEqual(response.content, JsonResponse(expected_data).content)


class ProjectModelsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.employee = Employee.objects.create(full_name="John Doe")
        self.project_confirmation = Project_Confirmation.objects.create(project_name="Test Project")
        self.project_job_assign = Project_Job_Assign.objects.create(project_confirmation=self.project_confirmation,job_assign_id="測試編號")
        self.project_employee_assign = Project_Employee_Assign.objects.create(project_job_assign=self.project_job_assign,construction_location="單元測試地點")

    def test_project_confirmation_detail_view(self):
        url = reverse('project_confirmation_api')
        request = self.factory.get(url, {'id': self.project_confirmation.id})
        response = Project_Confirmation_View.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_job_assign_detail_view(self):
        url = reverse('job_assign_api')
        request = self.factory.get(url, {'id': self.project_job_assign.id})
        response = Job_Assign_View.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_project_employee_assign_detail_view(self):
        url = reverse('project_employee_assign_api')
        request = self.factory.get(url, {'id': self.project_employee_assign.id})
        response = Project_Employee_Assign_View.as_view()(request)
        self.assertEqual(response.status_code, 200)