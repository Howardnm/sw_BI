from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import PerformanceModelForm
from app01.utils.pagination import Pagination


def performance_list(request):
    """ 个人业绩信息列表 """
    data_dict = {}
    search_name = request.GET.get("search_name", "")  # 有值传值，没值传空
    search_month = request.GET.get("search_month", "")  # 有值传值，没值传空
    if search_name:
        data_dict["name__name__contains"] = search_name  # __contains：指mobile的值包含变量search_data的字符串，即可搜出
        # "name__name__contains",第一个name是本表字段名，第二个name是跨表的字段名
    if search_month:
        data_dict["month__contains"] = search_month + "-01"  # __contains：指mobile的值包含变量search_data的字符串，即可搜出

    # select * from 表 order by level desc;【Django中：-id是desc, id是asc】
    queryset = models.Performance.objects.filter(**data_dict).order_by("month")
    page_obj = Pagination(request, queryset, "page", 12)
    context = {
        "search_name": search_name,  # 搜索框保留搜索值
        "search_month": search_month,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "performance_list.html", context)


def performance_add(request):
    """ 添加个人业绩信息 """
    if request.method == 'GET':
        form = PerformanceModelForm()
        return render(request, "performance_add.html", {"form": form})

    post_data = request.POST.copy()
    post_data["month"] = post_data.get("month") + "-01"
    # 用户POST提交数据，数据校验。
    form = PerformanceModelForm(data=post_data)
    if form.is_valid():
        form.save()
        return redirect("/performance/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "performance_add.html", {"form": form})


def performance_edit(request, nid):
    """ 编辑个人业绩信息 """
    obj = models.Performance.objects.filter(id=nid).first()
    if request.method == "GET":
        # 将 '2025-02-01' 转换为 '2025-02'
        initial_data = {
            "month": obj.month.strftime("%Y-%m") if obj.month else ""
        }
        form = PerformanceModelForm(instance=obj, initial=initial_data)
        return render(request, "performance_edit.html", {"form": form})

    post_data = request.POST.copy()
    post_data["month"] = post_data.get("month") + "-01"  # post的是2025-02，必须 2025-02-01 才能合法输入到form
    form = PerformanceModelForm(data=post_data, instance=obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/performance/list")
    return render(request, "performance_edit.html", {"form": form})


def performance_delete(request, nid):
    """ 删除个人业绩信息 """
    models.Performance.objects.filter(id=nid).delete()
    return redirect("/performance/list")
