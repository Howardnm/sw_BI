from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import SalespersonModelForm
from app01.utils.pagination import Pagination
from app01.utils.form_btn_search import FormBtnSearch


def sales_person_list(request):
    """ 销售人员列表 """
    form = SalespersonModelForm()
    search_bar = FormBtnSearch(request, form)
    # select * from 表 order by level desc;【Django中：-id是desc, id是asc】
    queryset = models.Salesperson.objects.filter(**search_bar.filter()).order_by("id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "search_html": search_bar.html_modal(),  # 搜索框
        "search_js": search_bar.js(),  # 搜索框
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "sales_person_list.html", context)


def sales_person_add(request):
    """ 添加销售人员 """
    if request.method == 'GET':
        form = SalespersonModelForm()
        return render(request, "sales_person_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = SalespersonModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/salesperson/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "sales_person_add.html", {"form": form})


def sales_person_edit(request, nid):
    """ 编辑销售人员 """
    obj = models.Salesperson.objects.filter(id=nid).first()
    if request.method == "GET":
        form = SalespersonModelForm(instance=obj)
        return render(request, "sales_person_edit.html", {"form": form})

    form = SalespersonModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/salesperson/list")
    return render(request, "sales_person_edit.html", {"form": form})


def sales_person_delete(request, nid):
    """ 销售人员删除 """
    models.Salesperson.objects.filter(id=nid).delete()
    return redirect("/salesperson/list")
