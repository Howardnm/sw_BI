from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import AdminModelForm, AdminEditForm, AdminResetPwdModelForm
from app01.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """
    # 获取当前登录的用户的信息，这些信息在登录过程中，即运行 views.account.py 时，被写入到session
    # info: dict = request.session.get("info")
    # info.get("id")
    # info.get("name")

    data_dict = {}
    search_data = request.GET.get("q", "")  # 有值传值，没值传空
    if search_data:
        data_dict["username__contains"] = search_data  # __contains：包含

    queryset = models.Admin.objects.filter(**data_dict).order_by("id")
    page_obj = Pagination(request, queryset)
    context = {
        "n0": search_data,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    """ 添加管理员 """
    title = "新建管理员"

    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", {"title": title, "form": form})


def admin_edit(request, nid):
    """ 编辑管理员 """
    title = "编辑管理员"
    # 对象 / None
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return render(request, "error.html", {"msg": "数据不存在"})
    if request.method == "GET":
        form = AdminEditForm(instance=obj)
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminEditForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", {"title": title, "form": form})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list")


def admin_reset_pwd(request, nid):
    """ 重置密码 """
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return render(request, "error.html", {"msg": "数据不存在"})
    title = f"【{obj.username}】重置密码"
    if request.method == "GET":
        form = AdminResetPwdModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminResetPwdModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", {"title": title, "form": form})
