from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import SalesTeamModelForm
from app01.utils.pagination import Pagination
from app01.utils.search_bar import SearchBar


def sales_team_list(request):
    """ 销售团队列表 """
    form = SalesTeamModelForm()
    search_bar = SearchBar(request, form)
    # select * from 表 order by level desc;【Django中：-id是desc, id是asc】
    queryset = models.SalesTeam.objects.filter(**search_bar.filter()).order_by("id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "search_html": search_bar.html(),  # 搜索框
        "search_js": search_bar.js(),  # 搜索框
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "sales_team_list.html", context)


def sales_team_add(request):
    """ 添加销售团队 """
    if request.method == 'GET':
        form = SalesTeamModelForm()
        return render(request, "sales_team_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = SalesTeamModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/salesteam/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "sales_team_add.html", {"form": form})


def sales_team_edit(request, nid):
    """ 编辑团队 """
    obj = models.SalesTeam.objects.filter(id=nid).first()
    if request.method == "GET":
        form = SalesTeamModelForm(instance=obj)
        return render(request, "sales_team_edit.html", {"form": form})

    form = SalesTeamModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/salesteam/list")
    return render(request, "sales_team_edit.html", {"form": form})


def sales_team_delete(request, nid):
    """ 销售团队删除 """
    models.SalesTeam.objects.filter(id=nid).delete()
    return redirect("/salesteam/list")
