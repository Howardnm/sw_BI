"""
用户管理
模块：增删改查
"""

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


def user_list(request):
    """ 用户列表 """
    queryset = models.Userinfo.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "n0": queryset,  # 搜索框保留搜索值
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """ 添加用户（原始方法） """
    if request.method == 'GET':
        context = {
            "gender_choices": models.Userinfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    name = request.POST.get('name')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    creat_time = request.POST.get('creat_time')
    gender_id = request.POST.get('gender_id')
    depart_id = request.POST.get('depart_id')
    print(name, password, age, account, creat_time, gender_id, depart_id)
    if name and password and creat_time:
        models.Userinfo.objects.create(name=name, password=password, age=age,
                                       account=account, create_time=creat_time,
                                       gender=gender_id, depart_id=depart_id)
    else:
        return render(request, "user_add.html")
    return redirect("/user/list")


# ################# ModelForm 示例 ###################


def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")

    # 校验失败（在页面上显示错误信息）
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    user_obj = models.Userinfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=user_obj)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=user_obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要添加一些值，是用户在网页不能输入的，可用以下方法
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ 用户删除 """
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/user/list")