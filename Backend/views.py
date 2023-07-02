from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse


def check_in(request):
    if request.method == 'POST':
        gps = request.POST.get('gps')
        # ip = request.POST.get('ip')
        # current_time =  request.POST.get('ip')
        print(gps)    
        #處理


    return JsonResponse({'status': 'success'})
