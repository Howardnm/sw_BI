from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.code import check_code
from app01.utils.form import LoginModelForm
from io import BytesIO


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginModelForm()
        return render(request, "login.html", {"form": form})
    form = LoginModelForm(data=request.POST, request=request)  # 传入 request，（request中有session的信息，其中包含图片验证码）
    if form.is_valid():
        # 验证码、用户名和密码正确
        request.session.pop("image_code", None)  # 删除 session 里的"验证码"键值对，防止用户拿着同一个验证码重复登录，从而无限延长 session 的有效期。
        # 网站生成随机sessionid：1、先把 sessionid 写到用户浏览器的cookie中 2、再把 {sessionid: session} 写入到服务器数据库中;
        request.session["info"] = {"id": form.instance.id, "name": form.instance.username}
        # 之后的html页面，可在html使用{{ request.session.info.name }}进行显示
        # 给session设置60s超时（这是给session整个对象进行设置超时，session里所有信息都会受到超时影响，超时后 session 内所有信息会清空）
        request.session.set_expiry(60 * 60 * 24 * 1000)  # 登录成功后，给session重新设置30天超时
        return redirect("/admin/list")
    return render(request, "login.html", {"form": form})


def image_code(request):
    """ 用于生成验证码图片 """
    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便后续获取用户输入的验证码进行校验）
    request.session["image_code"] = code_string
    # 给session设置60s超时（这是给session整个对象进行设置超时，session里所有信息都会受到超时影响，超时后 session 内所有信息会清空）
    request.session.set_expiry(60)

    # 把图片放入内存中
    stream = BytesIO()
    img.save(stream, "png")
    # stream.getvalue()  # 直接读取内容
    return HttpResponse(stream.getvalue(), content_type="image/png")


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login")


def register(request):
    return None
