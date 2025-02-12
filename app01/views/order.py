import random
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination


def order_list(request):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by("-id")
    page_obj = Pagination(request, queryset, "page")
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # html页码
    }
    return render(request, "order_list.html", context)


def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：由后台生成
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S%f") + str(random.randint(1000, 9999))  # 内部生成订单号，并写到form中，%f是6位浮点数（time函数最高精度）
        # 管理员：获取当前登录的管理员id
        form.instance.admin_id = request.session.get("info").get("id")  # 这个session信息需要在login的时候注入，否则为空
        form.save()
        return JsonResponse({"status": True})  # 直接传入dict，django会自动转json
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    if not models.Order.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    # 方法一
    # uid = request.GET.get("uid")
    # obj = models.Order.objects.filter(id=uid).first()  # 获得的是一个对象
    # if not obj:
    #     return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    # data_dict = {
    #     "status": True,
    #     "data": {
    #         "tittle": obj.tittle,
    #         "price": obj.price,
    #         "status": obj.status,
    #     }
    # }
    # return JsonResponse(data_dict)

    # 方法二
    uid = request.GET.get("uid")
    obj_dict = models.Order.objects.filter(id=uid).values("tittle", "price", "status").first()  # 获得的是一个字典
    # obj_dict = {"tittle": "1", "price": "22", "status": "1"}
    # obj_dict = models.Order.objects.filter(id=uid).values("tittle", "price")  # 获得的是一个列表,内嵌字典
    # obj_dict = [{"tittle": "1", "price": "22"}, {"tittle": "2", "price": "44"}, ]
    # obj_dict = models.Order.objects.filter(id=uid).values_list("id", "tittle")  # 获得的是一个列表,内嵌元组
    # obj_dict = [(1,"xx"), (2,"xxx"), ]
    if not obj_dict:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    data_dict = {
        "status": True,
        "data": obj_dict
    }
    return JsonResponse(data_dict)


def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    obj = models.Order.objects.filter(id=uid).first()
    if not obj:
        return JsonResponse({"status": False, "tips": "无法编辑，该行数据不存在，请刷新重试"})

    form = OrderModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})
