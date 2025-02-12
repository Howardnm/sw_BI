"""
部门管理
模块：增删改查
"""

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.pagination import Pagination  # 导入分页模块


def index(request):
    return render(request, "index.html")


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "n0": queryset,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request, "depart_add.html")

    depart_name = request.POST.get("depart_name")
    if depart_name:
        models.Department.objects.create(name=depart_name)
    return redirect("/depart/list")


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == "GET":
        depart = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"depart": depart})

    depart_name = request.POST.get("depart_name")
    if depart_name:
        models.Department.objects.filter(id=nid).update(name=depart_name)
    return redirect("/depart/list")


def depart_multi(request):
    """ 批量上传（excel文件） """
    from openpyxl import load_workbook
    # 1.获取用户上传的文件对象
    file_obj = request.FILES.get("upload_file")
    # 2.对象传递给openpyxl，又openpyxl读取文件的内容
    wb = load_workbook(file_obj)
    sheet = wb.worksheets[0]

    return redirect('/depart/list')
