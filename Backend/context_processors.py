from Backend.models import SysMessage

def sys_messages(request):
    get_sys_messages = SysMessage.objects.filter(Target_user=request.user.employee,watch=False)
    bottom_position = 20  # 初始底部位置
    sys_messages_data = []

    for msg in get_sys_messages:
        sys_messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'bottom': bottom_position
        })
        bottom_position += 70  # 递增底部位置


    return {'sys_messages': sys_messages_data}
