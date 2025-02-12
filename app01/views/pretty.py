"""
靓号管理
模块：增删改查
"""

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


def pretty_list(request):
    """ 靓号列表 """
    data_dict = {}
    search_data = request.GET.get("q", "")  # 有值传值，没值传空
    if search_data:
        data_dict["mobile__contains"] = search_data  # __contains：指mobile的值包含变量search_data的字符串，即可搜出

    # select * from 表 order by level desc;【Django中：-id是desc, id是asc】
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "n0": search_data,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """ 添加靓号 """
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """ 编辑用户 """
    obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/pretty/list")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """ 用户删除 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list")