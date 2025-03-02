from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import SalesDataModelForm
from app01.utils.pagination import Pagination
from app01.utils.search_bar import SearchBar


def salesdata_list(request):
    """ 销售大信息列表 """
    form = SalesDataModelForm()
    search_bar = SearchBar(request, form)
    queryset = models.SalesData.objects.filter(**search_bar.filter()).order_by("-id")
    page_obj = Pagination(request, queryset, "page", 12)
    context = {
        "search_html": search_bar.html(),  # 搜索框
        "search_js": search_bar.js(),  # 搜索框
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html(),  # html页码
    }
    return render(request, "salesdata_list.html", context)


def salesdata_add(request):
    return None


def salesdata_edit(request):
    return None


def salesdata_delete(request):
    return None
