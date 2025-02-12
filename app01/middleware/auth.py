"""
1、中间组件功能：
    可用于验证用户身份
2、应用中间件：(按列表顺序执行中间件)
    django 的 setting.py 添加：MIDDLEWARE += ['app02.middleware.auth.M1','app02.middleware.auth.M2',]
3、编写中间件函数：
    class M1(MiddlewareMixin):
        def process_request(self, request):
            return
        def process_response(self, request, response):
            return response
4、原理
    用户访问 --> process_request(M1)  --(返回None)--> process_request(M2) --(返回None)--> |~~~~~~~~~~~~~~~~~~~~|
                       |(有返回值）                          |(有返回值）                 | def index(request) |
    用户响应 <-- process_response(M1) <------------- process_response(M2) <------------ |~~~~~~~~~~~~~~~~~~~~|
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):  # 请求
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info : 获取当前用户请求的URL "/login"
        if request.path_info in ["/login", "/image/code"]:
            return  # 等价于 return None

        # 1.读取当前访问的用户的session信息, 如果能读到，说明已登录过，就可以继续向后走。
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect("/login")

    def process_response(self, request, response):  # 响应
        return response
