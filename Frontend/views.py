from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
from django .contrib.auth.decorators import login_required
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Employee

# Create your views here.

#首頁
def index(request):
    # login_form = LoginForm()
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        auto_login = request.POST.get('auto-login') == 'on'
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            print("登入成功")
            login(request, user)
            if auto_login:
                # Create a long-term session for auto-login
                session = SessionStore()
                session['user_id'] = user.id
                session.set_expiry(1209600)  # Two weeks
                print("Save")
                print(session)
                session.save()
            return HttpResponseRedirect('/')
        
    context = {
        # 'login_form':login_form
    }

    return render(request, 'index/index.html', context)

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

# @receiver(post_save, sender=User)
# def create_employee(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_employee(sender, instance, **kwargs):
#     instance.employee.save()
