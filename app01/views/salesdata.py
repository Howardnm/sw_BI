from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import SalesDataModelForm
from app01.utils.pagination import Pagination


def salesdata_list(request):
    """ 销售大信息列表 """
    data_dict = {}
    search_data = request.GET.get("q", "")  # 有值传值，没值传空
    if search_data:
        data_dict["mobile__contains"] = search_data  # __contains：指mobile的值包含变量search_data的字符串，即可搜出

    queryset = models.SalesData.objects.filter(**data_dict).order_by("id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "n0": search_data,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "salesdata_list.html", context)


def salesdata_add(request):
    return None


def salesdata_edit(request):
    return None


def salesdata_delete(request):
    return None