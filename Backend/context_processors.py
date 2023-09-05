from Backend.models import SysMessage,Client
from django.contrib.auth.models import AnonymousUser

def sys_messages(request):
    if  isinstance(request.user, AnonymousUser):
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