import json

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.utils import ErrorDict

from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination


def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by("-id")
    page_obj = Pagination(request, queryset, "page")
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    return render(request, "task_list.html", context)


@csrf_exempt  # 免除 csrf_token 认证（如果不用这个，可以在html用脚本读取请求头的 csrf_token ，并在ajax进行POST提交）
def ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # 方法一：
    # json_string = json.dumps(data_dict)  # 转为json格式
    # return HttpResponse(json_string)  # 传入json
    # 方法二(推荐)：  # 输出后，ajax自动把json识别成对象，而不是字符串，方便引用
    return JsonResponse(data_dict)  # 直接传入dict，django会自动转json


def add(request):
    # 1.用户发送过来的数据进行校验
    form = TaskModelForm(data=request.POST, request=request)  # 传入 request，（request中有session的信息，其中包含图片验证码）
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)  # 直接传入dict，django会自动转json
    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict)
