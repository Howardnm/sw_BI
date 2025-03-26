from collections import defaultdict

from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, OuterRef, Subquery
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


def chart_list1(request):
    """ 数据统计页面 """
    this_time = time.strftime("%Y-%m-%d %H:%M:%S")
    this_year = time.strftime("%Y")
    this_month = time.strftime("%m").split("0")[-1]
    context = {
        "this_year": this_year,
        "this_month": this_month,
        "this_time": this_time,
    }
    return render(request, "chart1.html", context)


def chart_list2(request):
    return render(request, "chart.html")


def data_month_sales_volume():
    """
    每月销售量（吨）
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
    formatted_sales = [round(float(sales_dict.get(month, 0) / 1000), 0) for month in range(1, 13)]  # KG变吨后，银行模式的四舍五入到整数
    # [23200, 0, 5000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return formatted_sales


def data_month_sales_revenue():
    """
    每月销售额（万元）
    [100570.0, 102960.0, 5480.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    """
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(
            revenue=ExpressionWrapper(
                F("sales_volume") * F("net_unit_price"),
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
    formatted_sales = [round(float(dict1.get(month, 0) / 10000), 2) for month in range(1, 13)]  # 元变万元，round(num, 2) 把小数限制到2位
    # [100570.0, 102960.0, 5480.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return formatted_sales


def data_supply_company():
    """
    三基地每月销售量（kg）
    [{name: '广东基地', data: [3, 5, 1, 13]}, {name: '昆山基地', data: [14, 8, 8, 12]}, {name: '武汉基地', data: [0, 2, 6, 3]}]
    """
    sales_product_subquery = models.SalesProduct.objects.filter(
        k3=OuterRef("k3")  # 让子查询匹配主查询的 k3
    ).values("supply_company")[:1]  # 取匹配到的第一个 supply_company，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每个k3的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            supply_company=Subquery(sales_product_subquery),  # 用子查询获取 supply_company
        )
        .values("supply_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'supply_company': None, 'sales_volume__sum': 0}, {'month': datetime.date(2025, 1, 1), 'supply_company': '广东基地', 'sales_volume__sum': 3805459}, {'month': datetime.date(2025, 1, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 1146300}, {'month': datetime.date(2025, 1, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 929509}, {'month': datetime.date(2025, 2, 1), 'supply_company': '广东基地', 'sales_volume__sum': 462926}, {'month': datetime.date(2025, 2, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 164045}, {'month': datetime.date(2025, 2, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 102700}]>
    print(queryset)

    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)

    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        supply_company = item['supply_company'] or "未知基地"

        company_monthly_sales[supply_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 0)
    print(company_monthly_sales)

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    print(list1)
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    # 等价于：
    lll = """
    SELECT 
    sd.k3, 
    (SELECT sp.supply_company FROM sales_product sp WHERE sp.k3 = sd.k3 LIMIT 1) AS supply_company,
    sd.sales_volume
    FROM sales_data sd
    WHERE YEAR(sd.date) = '2025';

    """

    return list1


def chat_api1(request):
    formatted_sales = data_month_sales_volume()

    data_dict = {
        "status": True,
        "data": {
            "title": "每月销售量",
            "xAxis": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            "yAxis": {"left": "吨", "right": ""},
            "series": {
                "a": {
                    "name": "目标销售量",
                    "data": [3000, 1000, 2000, 3000, 3000, 1000, 2000, 3000, 3000, 1000, 2000, 3000, ],
                    "valuePrefix": ' ',
                    "valueSuffix": ' 吨',
                    "yAxis": 0,  # 0为左轴，1为右轴
                },
                "b": {
                    "name": "实际销售量",
                    "data": formatted_sales,
                    "valuePrefix": ' ',
                    "valueSuffix": ' 吨',
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
            "title": "每月销售额",
            "xAxis": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            "yAxis": {"left": "万元", "right": ""},
            "series": {
                "a": {
                    "name": "目标销售额",
                    "data": [1000, 2000, 1500, 1000, 2000, 1500, 1000, 2000, 1500, 1000, 2000, 1500, ],
                    "valuePrefix": ' ',
                    "valueSuffix": ' 万元',
                    "yAxis": 0,  # 0为左轴，1为右轴
                },
                "b": {
                    "name": "实际销售额",
                    "data": formatted_sales,
                    "valuePrefix": ' ',
                    "valueSuffix": ' 万元',
                    "yAxis": 0,
                },
            },
        }
    }
    return JsonResponse(data_dict)


def chat_api3(request):
    list = data_supply_company()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)
