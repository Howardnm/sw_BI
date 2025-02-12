from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart.html")


def chart_bar(request):
    """ 构造柱状图数据 """
    data_dict = {
        "legend": ['销量', '业绩'],
        "x_axis": ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
        "series": [
            {
                "name": '销量',
                "type": 'bar',
                "data": [5, 20, 36, 10, 10, 20]
            },
            {
                "name": '业绩',
                "type": 'bar',
                "data": [55, 10, 66, 20, 20, 10]
            }
        ],
    }

    return JsonResponse({"status": True, "data": data_dict})
