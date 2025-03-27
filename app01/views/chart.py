from collections import defaultdict

from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, OuterRef, Subquery, Q
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
    formatted_sales = [round(float(sales_dict.get(month, 0) / 1000), 2) for month in range(1, 13)]  # KG变吨后，银行模式的四舍五入到整数
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
    三基地每月销售量（吨）
    [{name: '广东基地', data: [3, 5, 1, 13]}, {name: '昆山基地', data: [14, 8, 8, 12]}, {name: '武汉基地', data: [0, 2, 6, 3]}]
    """
    # 生成：每个月每基地的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        # .annotate(
        #     supply_company=Subquery(sales_product_subquery),  # 用子查询获取 supply_company
        # )
        .values("supply_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'supply_company': None, 'sales_volume__sum': 0}, {'month': datetime.date(2025, 1, 1), 'supply_company': '广东基地', 'sales_volume__sum': 3805459}, {'month': datetime.date(2025, 1, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 1146300}, {'month': datetime.date(2025, 1, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 929509}, {'month': datetime.date(2025, 2, 1), 'supply_company': '广东基地', 'sales_volume__sum': 462926}, {'month': datetime.date(2025, 2, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 164045}, {'month': datetime.date(2025, 2, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 102700}]>
    # 等价于：
    lll = """
    SELECT 
    sd.k3, 
    (SELECT sp.supply_company FROM sales_product sp WHERE sp.k3 = sd.k3 LIMIT 1) AS supply_company,
    sd.sales_volume
    FROM sales_data sd
    WHERE YEAR(sd.date) = '2025';

    """
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        supply_company = item['supply_company'] or "未知基地"
        company_monthly_sales[supply_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 0)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    # [{'name': '未知基地', 'data': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'name': '广东基地', 'data': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'name': '昆山基地', 'data': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'name': '武汉基地', 'data': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_supply_company_raw_material():
    """
    三基地每月原料销售量（吨）
    [{name: '广东基地', data: [3, 5, 1, 13]}, {name: '昆山基地', data: [14, 8, 8, 12]}, {name: '武汉基地', data: [0, 2, 6, 3]}]
    """
    sales_product_subquery = models.SalesProduct.objects.filter(
        actual_client_company=OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        k3=OuterRef("k3")  # 让子查询匹配主查询的 k3
    ).values("product_domain_groups")[:1]  # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_domain_groups=Subquery(sales_product_subquery),  # 用子查询获取 product_domain_groups
        )
        .filter(product_domain_groups="原料销售")
        .values("supply_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'supply_company': None, 'sales_volume__sum': 0}, {'month': datetime.date(2025, 1, 1), 'supply_company': '广东基地', 'sales_volume__sum': 3805459}, {'month': datetime.date(2025, 1, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 1146300}, {'month': datetime.date(2025, 1, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 929509}, {'month': datetime.date(2025, 2, 1), 'supply_company': '广东基地', 'sales_volume__sum': 462926}, {'month': datetime.date(2025, 2, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 164045}, {'month': datetime.date(2025, 2, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 102700}]>
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        supply_company = item['supply_company'] or "未知基地"
        company_monthly_sales[supply_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_supply_company_intra_sales():
    """
    三基地每月内销，销售量（吨）
    [{name: '广东基地', data: [3, 5, 1, 13]}, {name: '昆山基地', data: [14, 8, 8, 12]}, {name: '武汉基地', data: [0, 2, 6, 3]}]
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_domain_groups")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_domain_groups=Subquery(sales_product_subquery),  # 用子查询获取 product_domain_groups
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(~Q(product_domain_groups="原料销售"), intra_or_external_sales="内销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("supply_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'supply_company': None, 'sales_volume__sum': 0}, {'month': datetime.date(2025, 1, 1), 'supply_company': '广东基地', 'sales_volume__sum': 3805459}, {'month': datetime.date(2025, 1, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 1146300}, {'month': datetime.date(2025, 1, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 929509}, {'month': datetime.date(2025, 2, 1), 'supply_company': '广东基地', 'sales_volume__sum': 462926}, {'month': datetime.date(2025, 2, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 164045}, {'month': datetime.date(2025, 2, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 102700}]>
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        supply_company = item['supply_company'] or "未知基地"
        company_monthly_sales[supply_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_supply_company_external_sales():
    """
    三基地每月外销，销售量（吨）
    [{name: '广东基地', data: [3, 5, 1, 13]}, {name: '昆山基地', data: [14, 8, 8, 12]}, {name: '武汉基地', data: [0, 2, 6, 3]}]
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_domain_groups")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_domain_groups=Subquery(sales_product_subquery),  # 用子查询获取 product_domain_groups
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(~Q(product_domain_groups="原料销售"), intra_or_external_sales="外销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("supply_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # <QuerySet [{'month': datetime.date(2025, 1, 1), 'supply_company': None, 'sales_volume__sum': 0}, {'month': datetime.date(2025, 1, 1), 'supply_company': '广东基地', 'sales_volume__sum': 3805459}, {'month': datetime.date(2025, 1, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 1146300}, {'month': datetime.date(2025, 1, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 929509}, {'month': datetime.date(2025, 2, 1), 'supply_company': '广东基地', 'sales_volume__sum': 462926}, {'month': datetime.date(2025, 2, 1), 'supply_company': '昆山基地', 'sales_volume__sum': 164045}, {'month': datetime.date(2025, 2, 1), 'supply_company': '武汉基地', 'sales_volume__sum': 102700}]>
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        supply_company = item['supply_company'] or "未知基地"
        company_monthly_sales[supply_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_product_domain_groups_intra_sales():
    """
    组别内销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_domain_groups")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_domain_groups=Subquery(sales_product_subquery),  # 用子查询获取 product_domain_groups
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="内销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("product_domain_groups", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        product_domain_groups = item['product_domain_groups'] or "未知组别"
        company_monthly_sales[product_domain_groups][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_product_domain_groups_external_sales():
    """
    组别外销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_domain_groups")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_domain_groups=Subquery(sales_product_subquery),  # 用子查询获取 product_domain_groups
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="外销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("product_domain_groups", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        product_domain_groups = item['product_domain_groups'] or "未知组别"
        company_monthly_sales[product_domain_groups][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_product_category_intra_sales():
    """
    产品线内销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_category")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_category=Subquery(sales_product_subquery),  # 用子查询获取 product_category
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="内销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("product_category", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        product_category = item['product_category'] or "未知组别"
        company_monthly_sales[product_category][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_product_category_external_sales():
    """
    产品线外销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("product_category")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            product_category=Subquery(sales_product_subquery),  # 用子查询获取 product_category
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="外销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("product_category", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        product_category = item['product_category'] or "未知组别"
        company_monthly_sales[product_category][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_core_product_intra_sales():
    """
    主打产品-内销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("core_product")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            core_product=Subquery(sales_product_subquery),  # 用子查询获取 product_category
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="内销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("core_product", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        core_product = item['core_product'] or "未知组别"
        company_monthly_sales[core_product][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_core_product_external_sales():
    """
    主打产品-外销，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("core_product")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            core_product=Subquery(sales_product_subquery),  # 用子查询获取 product_category
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .filter(intra_or_external_sales="外销")  # .filter(~Q(...))，反选，排除原料销售的数据
        .values("core_product", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        core_product = item['core_product'] or "未知组别"
        company_monthly_sales[core_product][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = []
    for key, value in company_monthly_sales.items():
        list1.append({
            "name": key,
            "data": value
        })
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    return list1


def data_actual_client_company_intra_sales():
    """
    客户，销售量（吨）
    """
    # 公共的过滤条件，避免重复代码
    filter_args = {
        "actual_client_company": OuterRef("client_company"),  # 让子查询匹配主查询的 实际购货单位
        "k3": OuterRef("k3"),  # 让子查询匹配主查询的 k3
    }
    # 子查询：获取产品领域组别
    sales_product_subquery = models.SalesProduct.objects.filter(**filter_args).values("actual_client_company")[:1]
    # 取匹配到的第一个 组别（家电、原料销售），只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。
    # 子查询：获取内外销标识
    intra_or_external_sales_subquery = models.SalesProduct.objects.filter(**filter_args).values("intra_or_external_sales")[:1]
    # 取匹配到的第一个 内外销，只取第一条数据，但仍是 QuerySet。不能用.first() 因为这是提前执行查询，数据已取出，Django 不能嵌套进 SQL。

    # 生成：每个月每基地原料的出货量
    queryset: list = (
        models.SalesData.objects
        .filter(date__year=time.strftime("%Y"))
        .annotate(month=TruncMonth("date"))  # 新建月份字段（实际上就是把date的日都变为1号，然后新建个month字段来储存）
        .annotate(
            actual_client_company=Subquery(sales_product_subquery),  # 用子查询获取 product_category
            intra_or_external_sales=Subquery(intra_or_external_sales_subquery),
        )
        .values("actual_client_company", "month")  # 只显示month, k3字段
        .annotate(
            sales_volume__sum=Sum("sales_volume"),  # 根据上一行处理后的字典列表，对于相同字典进行合并，并新增一个sales_volume__sum字段在字典中，并把计算好的值插入其中。
        )
        .order_by("month")
    )
    # print(queryset)
    # 统计各个 supply_company 1-12 月的销售数据
    company_monthly_sales = defaultdict(lambda: [0] * 12)
    for item in queryset:
        month_index = item['month'].month - 1  # 1 月 -> 索引 0, 2 月 -> 索引 1 ...
        actual_client_company = item['actual_client_company'] or "未知"
        company_monthly_sales[actual_client_company][month_index] += round(float(item['sales_volume__sum'] / 1000), 1)
    # defaultdict(<function data_supply_company.<locals>.<lambda> at 0x000002DB74F8C4C0>, {'未知基地': [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '广东基地': [3805.0, 463.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '昆山基地': [1146.0, 164.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '武汉基地': [930.0, 103.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    list1 = [['客户', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'], ]
    for key, value in company_monthly_sales.items():
        data1 = []
        data1.append(key)
        data1.extend(value)
        list1.append(data1)
    """
    [{name: 'Road', data: [434, 290, 307]}, {name: 'Rail', data: [272, 153, 156]}, {name: 'Air', data: [13, 7, 8]}, {name: 'Sea',data: [55, 35, 41]}]
    """
    print(list1)
    import pandas as pd
    # 创建 DataFrame 并转置
    df = pd.DataFrame(list1[1:], columns=list1[0]).set_index('客户').T

    # 转为列表嵌套列表（含列名）
    result = [df.columns.tolist()] + df.values.tolist()
    print(result)
    return result


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


def chat_api4(request):
    list = data_supply_company_raw_material()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api5(request):
    list = data_supply_company_intra_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api6(request):
    list = data_supply_company_external_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api7(request):
    list = data_product_domain_groups_intra_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api8(request):
    list = data_product_domain_groups_external_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api9(request):
    list = data_product_category_intra_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api10(request):
    list = data_product_category_external_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api11(request):
    list = data_core_product_intra_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api12(request):
    list = data_core_product_external_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)


def chat_api13(request):
    list = data_actual_client_company_intra_sales()
    data_dict = {
        "status": True,
        "data": {
            "series": list
        }
    }
    return JsonResponse(data_dict)
