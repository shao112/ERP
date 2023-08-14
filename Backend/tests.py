from django.test import TestCase, RequestFactory,TransactionTestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import Project_Confirmation,Employee  # 假设您有合适的模型
from .views import Project_Confirmation_View
from django.contrib.auth.models import User
from . import views

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
        print(self.employee_1)
        print(self.employee_1.id)
        request = self.factory.get(url, {'id': self.employee_1.id})

        # 调用视图函数
        response = views.Employee_View.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # 断言返回的 JSON 数据是否正确
        # expected_data = {
        #     # 预期的数据，根据您的记录内容进行修改
        # }
        # self.assertJSONEqual(response.content, JsonResponse(expected_data).content)

