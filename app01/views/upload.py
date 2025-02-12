from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models


def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    # print(request.POST)  # 请求体中的数据
    # <QueryDict: {'csrfmiddlewaretoken': ['i5BzGvgiHYMGB5dUPvE5znnSThmH8Vig3mPKwWclmwNqkn5PbKAFgx3NukYo6p1d'], 'username': ['']}>
    # print(request.FILES)  # 请求发过来的文件
    # <MultiValueDict: {'avatar': [<InMemoryUploadedFile: 新建文本文档.txt (text/plain)>]}>

    file_obj = request.FILES.get("avatar")
    # print(file_obj.name)  # 取得文件名
    f = open(file_obj.name, mode="wb")
    for chunk in file_obj.chunks():  # file_obj.chunks 文件分块读取
        f.write(chunk)
    f.close()

    return render(request, "upload_list.html")
