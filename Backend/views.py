from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed
import json
from datetime import datetime

from .models import Clock


def check_in(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        gps = data.get('gps')
        clock_in_or_out = data.get('clock_in_or_out')
        clock_time = data.get('clock_time')
        clock_time = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%fZ')

        Clock.objects.create(
            employee_id=request.user.employee,
            clock_time=clock_time,
            clock_in_or_out=clock_in_or_out,
            clock_GPS=gps
        )

        return JsonResponse({'status': 'success'})

    return HttpResponseNotAllowed(['POST'])
