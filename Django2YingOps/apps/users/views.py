from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from utils.mixin_util import LoginRequiredMixin
from .forms import *
from assets.models import AssetsInfo


class IndexView(LoginRequiredMixin, View):
    """
    首页展示
    """

    def get(self, request):
        linux_count = AssetsInfo.objects.all().count()
        windows_count = 0
        switch_count = 0
        return render(request, 'index.html', locals())


class LoginView(View):
    """
    登录系统
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        userprofile_form = UserProfileForm(request.POST)
        if userprofile_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'index.html', locals())
            return render(request, 'login.html', {'msg': '登录：用户名或者密码错误'})
        return render(request, 'login.html', {'userprofile_form': userprofile_form})


class LogoutView(View):
    """
    登出系统
    """

    def get(self, request):
        logout(request)
        return render(request, 'login.html')


class UserInfo(LoginRequiredMixin, View):
    """
    用户信息
    """

    def get(self, request):
        userprofile = UserProfile.objects.all()
        return render(request, 'users/info.html', locals())

    def post(self, request):
        pass


class ModifyPwd(LoginRequiredMixin, View):
    """
    修改用户密码
    """

    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            userprofile = UserProfile.objects.get(username=request.user)
            if pwd1 != pwd2:
                msg = ' 密码不一致，请重新输入！'
                return render(request, 'users/info.html', locals())
            userprofile.password = make_password(pwd1)
            userprofile.save()
            return render(request, 'users/info.html', locals())
        return render(request, 'users/info.html', locals())


class RegisterView(View):
    """
    注册用户
    """

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = UserProfile()
            reg_email = request.POST.get('reg_email')
            username = request.POST.get('reg_username')
            phone = request.POST.get('phone')
            reg_password = request.POST.get('reg_password')
            rep_password = request.POST.get('rep_password')
            if reg_password != rep_password:
                msg = '注册用户：密码不一致，请重新输入！'
                return render(request, 'login.html', locals())
            user.email = reg_email
            user.phone = phone
            user.password = make_password(reg_password)
            if UserProfile.objects.filter(username=username):
                msg = "注册用户：该用户'{0}'已经存在，请重新输入！".format(username)
                return render(request, 'login.html', locals())
            user.username = username
            user.save()
            msg = '恭喜您{0}，注册成功，可以进行登录！'.format(username)
            return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())


class ForgetPwdView(View):
    def post(self, request):
        email = request.POST.get('forgetpwd', '')

        if UserProfile.objects.filter(Q(username=email) | Q(email=email)):
            user = UserProfile.objects.get(Q(username=email) | Q(email=email))
            user.password = make_password('123456')
            user.save()
            msg = '忘记密码：密码重置成功，密码为：123456'
            return render(request, 'login.html', locals())
        else:
            msg = "忘记密码：系统中没有该用户'{0}'".format(email)
            return render(request, 'login.html', locals())
