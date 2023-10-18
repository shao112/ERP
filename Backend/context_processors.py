from Backend.models import SysMessage,Client,ApprovalModel
from django.contrib.auth.models import AnonymousUser

from django.conf import settings


def approval_count(request):
    if  isinstance(request.user, AnonymousUser):
        return {'approval_count': 0}
    
    if hasattr( request.user,"employee")==False:
        return {'approval_count': "異常"}

    current_employee = request.user.employee

    related_records = []

    for Approval in ApprovalModel.objects.filter(current_status="in_process"):            
        get_employee = Approval.get_approval_employee()
        if get_employee !="x":
            if  get_employee ==current_employee :
                related_records.append(Approval)
        elif get_employee =="clean":
            pass
        else:
            try:
            # 取得作者部門
                get_createdby = Approval.get_created_by
                if get_createdby:
                    department =get_createdby.departments
                    #撈取主管權限的員工
                    supervisor_employees = department.employees.filter(user__groups__name='主管').values_list('id', flat=True)
                    #判斷主管是不是在當前user
                    is_supervisor = current_employee.id in supervisor_employees
                    if is_supervisor:            
                        related_records.append(Approval)
            except Exception as e:
                return {"approval_count":"未輸入部門"}
    return {"approval_count":len(related_records)}



def pass_test_func(request):
    pass_test_func = settings.PASS_TEST_FUNC

    return {"pass_test_func":pass_test_func}

def sys_messages(request):
    if  isinstance(request.user, AnonymousUser):
        return {'sys_messages': {}}
    if hasattr( request.user,"employee")==False:
        return {'sys_messages': {}}

    get_sys_messages = SysMessage.objects.filter(Target_user=request.user.employee,watch=False)
    bottom_position = 20  # 初始底部位置
    sys_messages_data = []

    for msg in get_sys_messages:
        sys_messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'bottom': bottom_position
        })
        bottom_position += 70 

    return {'sys_messages': sys_messages_data}


def client_list(request):
    clients = Client.objects.all()
    return {'clients': clients}