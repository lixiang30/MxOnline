from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    """
    基于类的登录
    """
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        # 获取用户提交的用户名和密码
        user_name = request.POST.get('username',None)
        pass_word = request.POST.get('password',None)

        user = authenticate(username=user_name,password=pass_word)
        if user is not None:
            login(request,user)
            return render(request,"index.html")
        else:
            return render(request,"login.html",{'msg':'用户名或密码错误！'})



def user_login(request):
    """
    基于函数的登录
    :param request:
    :return:
    """
    # 判断用户登录方式是否是POST
    if request.method == "POST":
        # 获取用户提交的用户名和密码
        user_name = request.POST.get('username', None)
        pass_word = request.POST.get('password', None)
        # 成功返回user对象,失败None
        user = authenticate(username=user_name, password=pass_word)
        # 如果不是null说明验证成功
        if user is not None:
            # 登录
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
    elif request.method == "GET":
        return render(request,"login.html",{})
