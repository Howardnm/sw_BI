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
    salesindicator, salesdata, salesproduct

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
    path('', chart.chart_salesindicator_sales_revenue),

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
    path('chart/list1', chart.chart_list1),
    path('chart/chart_supply_company', chart.chart_supply_company),
    path('chart/chart_salesindicator_sales_revenue', chart.chart_salesindicator_sales_revenue),

    # api销售量
    path('chart/api/1', chart.chat_api1),
    path('chart/api/2', chart.chat_api2),
    path('chart/api/3', chart.chat_api3),
    path('chart/api/4', chart.chat_api4),
    path('chart/api/5', chart.chat_api5),
    path('chart/api/6', chart.chat_api6),
    path('chart/api/7', chart.chat_api7),
    path('chart/api/8', chart.chat_api8),
    path('chart/api/9', chart.chat_api9),
    path('chart/api/10', chart.chat_api10),
    path('chart/api/11', chart.chat_api11),
    path('chart/api/12', chart.chat_api12),
    path('chart/api/13', chart.chat_api13),
    # api销售额
    path('chart/api_1/1', chart.api_revenue_1),
    path('chart/api_1/2', chart.api_revenue_2),
    path('chart/api_1/3', chart.api_revenue_3),
    path('chart/api_1/4', chart.api_revenue_4),
    # api全年总数
    path('chart/api/api_year_sales_volume', chart.api_year_sales_volume),
    path('chart/api/api_year_sales_volume_target', chart.api_year_sales_volume_target),
    path('chart/api/api_year_sales_revenue', chart.api_year_sales_revenue),
    path('chart/api/api_year_sales_revenue_target', chart.api_year_sales_revenue_target),
    path('chart/api/api_year_new_client_company', chart.api_year_new_client_company),
    # 业务员指标达成
    path('chart/api/api_SalesIndicator_sales_volume_sanking', chart.api_SalesIndicator_sales_volume_sanking),
    path('chart/api/api_SalesIndicator_team_sales_volume_sanking', chart.api_SalesIndicator_team_sales_volume_sanking),
    path('chart/api/api_SalesIndicator_sales_revenue_sanking', chart.api_SalesIndicator_sales_revenue_sanking),
    path('chart/api/api_SalesIndicator_team_sales_revenue_sanking', chart.api_SalesIndicator_team_sales_revenue_sanking),
    path('chart/api/api_this_month_SalesIndicator_sales_volume_sanking', chart.api_this_month_SalesIndicator_sales_volume_sanking),
    path('chart/api/api_this_month_SalesIndicator_team_sales_volume_sanking', chart.api_this_month_SalesIndicator_team_sales_volume_sanking),
    path('chart/api/api_this_month_SalesIndicator_sales_revenue_sanking', chart.api_this_month_SalesIndicator_sales_revenue_sanking),
    path('chart/api/api_this_month_SalesIndicator_team_sales_revenue_sanking', chart.api_this_month_SalesIndicator_team_sales_revenue_sanking),

    # 上传文件
    path('upload/list', upload.upload_list),

    # 销售团队
    path('salesteam/list', salesteam.list),
    path('salesteam/add', salesteam.add),
    path('salesteam/edit', salesteam.edit),
    path('salesteam/edit_detail', salesteam.edit_detail),
    path('salesteam/delete', salesteam.delete),
    path('salesteam/delete_all', salesteam.delete_all),
    # 销售人员
    path('salesperson/list', salesperson.list),
    path('salesperson/add', salesperson.add),
    path('salesperson/edit', salesperson.edit),
    path('salesperson/edit_detail', salesperson.edit_detail),
    path('salesperson/delete', salesperson.delete),
    path('salesperson/delete_all', salesperson.delete_all),
    # 个人业绩信息
    path('salesindicator/list', salesindicator.list),
    path('salesindicator/add', salesindicator.add),
    path('salesindicator/edit', salesindicator.edit),
    path('salesindicator/edit_detail', salesindicator.edit_detail),
    path('salesindicator/delete', salesindicator.delete),
    path('salesindicator/delete_all', salesindicator.delete_all),
    path('salesindicator/addform', salesindicator.addform),
    # 客户产品信息
    path('salesproduct/list', salesproduct.list),
    path('salesproduct/add', salesproduct.add),
    path('salesproduct/edit', salesproduct.edit),
    path('salesproduct/edit_detail', salesproduct.edit_detail),
    path('salesproduct/delete', salesproduct.delete),
    path('salesproduct/delete_all', salesproduct.delete_all),
    path('salesproduct/addform', salesproduct.addform),
    # 销售大信息
    path('salesdata/list', salesdata.salesdata_list),
    path('salesdata/add', salesdata.salesdata_add),
    path('salesdata/edit', salesdata.salesdata_edit),
    path('salesdata/edit_detail', salesdata.salesdata_edit_detail),
    path('salesdata/delete', salesdata.salesdata_delete),
    path('salesdata/delete_all', salesdata.salesdata_delete_all),
    path('salesdata/addform', salesdata.salesdata_addform),

]
