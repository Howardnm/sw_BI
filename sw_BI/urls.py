"""
URL configuration for Django_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from app01 import views
from app01.views import depart, user, pretty, admin, account, task, order, chart, upload, salesperson, salesteam, \
    performance, salesdata

urlpatterns = [
    # path('silk/', include('silk.urls', namespace='silk')),
    # path('admin/', admin.site.urls),

    # app01
    # path('index/', views.index),
    # path('user_list/', views.user_list),
    # path('user_add/', views.user_add),
    # path('tql/', views.tql),
    # path('news/', views.news),
    # path('something/', views.something),
    #
    # # 用户登录
    # path('login/', views.login),
    # path('orm/', views.orm),
    #
    # # 案例：用户管理
    # path('info/list', views.info_list),
    # path('info/add', views.info_add),
    # path('info/delete', views.info_delete),

    # app02
    # 首页
    path('', chart.chart_list),

    # 登录
    path('login', account.login),
    path('image/code', account.image_code),
    path('register', account.register),
    path('logout', account.logout),

    # 管理员列表
    path('admin/list', admin.admin_list),
    path('admin/add', admin.admin_add),
    path('admin/<int:nid>/edit', admin.admin_edit),
    path('admin/<int:nid>/delete', admin.admin_delete),
    path('admin/<int:nid>/reset_pwd', admin.admin_reset_pwd),

    # 部门列表
    path('depart/list', depart.depart_list),
    path('depart/add', depart.depart_add),
    path('depart/delete', depart.depart_delete),
    path('depart/<int:nid>/edit', depart.depart_edit),
    path('depart/multi', depart.depart_multi),

    # 用户列表
    path('user/list', user.user_list),
    path('user/add', user.user_add),
    path('user/model/form/add', user.user_model_form_add),
    path('user/<int:nid>/edit', user.user_edit),
    path('user/<int:nid>/delete', user.user_delete),

    # 靓号列表
    path('pretty/list', pretty.pretty_list),
    path('pretty/add', pretty.pretty_add),
    path('pretty/<int:nid>/edit', pretty.pretty_edit),
    path('pretty/<int:nid>/delete', pretty.pretty_delete),

    # 任务管理
    path('task/list', task.task_list),
    path('task/ajax', task.ajax),
    path('task/add', task.add),

    # 订单管理
    path('order/list', order.order_list),
    path('order/add', order.order_add),
    path('order/delete', order.order_delete),
    path('order/detail', order.order_detail),
    path('order/edit', order.order_edit),

    # 数据统计
    path('chart/list', chart.chart_list),
    path('chart/bar', chart.chart_bar),

    # 上传文件
    path('upload/list', upload.upload_list),

    # 销售团队
    path('salesteam/list', salesteam.sales_team_list),
    path('salesteam/add', salesteam.sales_team_add),
    path('salesteam/<int:nid>/edit', salesteam.sales_team_edit),
    path('salesteam/<int:nid>/delete', salesteam.sales_team_delete),
    # 销售人员
    path('salesperson/list', salesperson.sales_person_list),
    path('salesperson/add', salesperson.sales_person_add),
    path('salesperson/<int:nid>/edit', salesperson.sales_person_edit),
    path('salesperson/<int:nid>/delete', salesperson.sales_person_delete),
    # 个人业绩信息
    path('performance/list', performance.performance_list),
    path('performance/add', performance.performance_add),
    path('performance/<int:nid>/edit', performance.performance_edit),
    path('performance/<int:nid>/delete', performance.performance_delete),
    # 销售大信息
    path('salesdata/list', salesdata.salesdata_list),
    path('salesdata/add', salesdata.salesdata_add),
    path('salesdata/<int:nid>/edit', salesdata.salesdata_edit),
    path('salesdata/<int:nid>/delete', salesdata.salesdata_delete),

]
