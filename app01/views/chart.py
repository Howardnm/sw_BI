from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models
import time
import pandas as pd


def chart_list(request):
    """ 数据统计页面 """
    this_time = time.strftime("%Y-%m-%d %H:%M:%S")
    this_year = time.strftime("%Y")
    this_month = time.strftime("%m").split("0")[-1]
    context = {
        "this_year": this_year,
        "this_month": this_month,
        "this_time": this_time,
    }
    return render(request, "chart.html", context)


def chart_bar(request):
    """ 构造柱状图数据 """
    this_year = time.strftime("%Y")
    monthly_sales = []
    for i in range(12):
        month = f"{this_year}-{i + 1:02d}-01"
        queryset: list = models.Performance.objects.filter(month=month).values()
        df = pd.DataFrame(queryset)
        monthly_sales.append(str(df.get('sales_revenue', pd.Series([0] * len(df))).fillna(0).sum()))
        # 如果 target 存在 → 直接 .fillna(0).sum()
        # 如果 target 不存在 → df.get('target') 返回 全 0 的 Series，避免 NoneType 错误。
    # print(monthly_sales)
    data_dict = {
        "legend": ['销量', '业绩', '销售额', '销售额1'],
        "x_axis": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        "data1": monthly_sales,
        "data2": [500, 400, 800, 1000, ],
    }

    return JsonResponse({"status": True, "data": data_dict})
