from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
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


def chart_list2(request):
    return render(request, "chart.html")


def data_month_sales_volume():
    """
    每月销售吨数
    [23200, 0, 5000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """
    # 等价于 "SELECT date AS month, sum(sales_volume) FROM SalesData GROUP BY month ORDER BY month"
    monthly_sales_volume = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))  # 只筛选当前年的数据
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .values("month")  # 只显示month字段
        .annotate(Sum("sales_volume"))  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        .order_by("month")  # 按月份排序
    )
    # < QuerySet[{'month': datetime.date(2025, 1, 1), 'sales_volume__sum': 23200}, {'month': datetime.date(2025, 3, 1), 'sales_volume__sum': 5000}] >
    sales_dict = {item["month"].month: item["sales_volume__sum"] for item in monthly_sales_volume}  # .month是取日期的月份
    # {1: 23200, 3: 5000}
    formatted_sales = [sales_dict.get(month, 0) for month in range(1, 13)]
    # [23200, 0, 5000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return formatted_sales


def data_month_sales_revenue():
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(
            revenue=ExpressionWrapper(
                F("sales_volume") * F("gross_unit_price"),
                output_field=DecimalField()
            )
        )
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(Sum("revenue"))
        .order_by("month")
    )
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'revenue__sum': Decimal('100570.00000000000000')}, {'month': datetime.date(2025, 2, 1), 'revenue__sum': Decimal('102960.00000000000000')}, {'month': datetime.date(2025, 3, 1), 'revenue__sum': Decimal('5480.50000000000000')}]>
    dict1 = {item["month"].month: item["revenue__sum"] for item in queryset}
    # {1: Decimal('100570.00000000000000'), 2: Decimal('102960.00000000000000'), 3: Decimal('5480.50000000000000')}
    formatted_sales = [float(dict1.get(month, 0)) for month in range(1, 13)]
    # [100570.0, 102960.0, 5480.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return formatted_sales


def chat_api1(request):
    formatted_sales = data_month_sales_volume()

    data_dict = {
        "status": True,
        "data": {
            "title": "销售量",
            "xAxis": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            "yAxis": {"left": "左纵坐标标题""", "right": ""},
            "series": {
                "a": {
                    "name": "业绩目标",
                    "data": [10000, 20000, 30000, 10000, 20000, 30000, 10000, 20000, 30000, 10000, 20000, 30000, ],
                    "valuePrefix": ' ',
                    "valueSuffix": ' Kg',
                    "yAxis": 0,  # 0为左轴，1为右轴
                },
                "b": {
                    "name": "实际业绩",
                    "data": formatted_sales,
                    "valuePrefix": ' ',
                    "valueSuffix": ' Kg',
                    "yAxis": 0,
                },
            },
        }
    }
    return JsonResponse(data_dict)


def chat_api2(request):
    formatted_sales = data_month_sales_revenue()
    data_dict = {
        "status": True,
        "data": {
            "title": "销售额",
            "xAxis": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            "yAxis": {"left": "左纵坐标标题""", "right": ""},
            "series": {
                "a": {
                    "name": "业绩目标",
                    "data": [10000, 20000, 30000, 10000, 20000, 30000, 10000, 20000, 30000, 10000, 20000, 30000, ],
                    "valuePrefix": ' ',
                    "valueSuffix": ' 元',
                    "yAxis": 0,  # 0为左轴，1为右轴
                },
                "b": {
                    "name": "实际业绩",
                    "data": formatted_sales,
                    "valuePrefix": ' ',
                    "valueSuffix": ' 元',
                    "yAxis": 0,
                },
            },
        }
    }
    return JsonResponse(data_dict)
