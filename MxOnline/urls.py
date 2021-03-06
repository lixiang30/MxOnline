"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
# from users.views import user_login
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from organization.views import OrgView
from django.views.static import serve # 处理静态文件
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    # url('^login/$',user_login,name='login'), #　基于函数视图，这样配置url
    url('^login/$',LoginView.as_view(),name="login"),
    url('^register/$',RegisterView.as_view(),name="register"),
    url('^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active'),
    url(r'^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_pwd'),
    url(r'^modify_pwd/(?P<active_code>.*)/$',ModifyPwdView.as_view(),name='modify_pwd'),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}), # 配置上传文件的访问处理函数

    url('^org/',include('organization.urls',namespace='org')), # 课程机构url设置

    #课程相关url配置
    url(r'^course/',include('courses.urls',namespace="course")),

]
