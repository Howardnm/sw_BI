import time

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import SalesDataModelForm
from app01.utils.form_btn_delete import FormBtnDelete
from app01.utils.form_btn_upload import FormBtnUpload
from app01.utils.pagination import Pagination
from app01.utils.search_bar import SearchBar


def salesdata_list(request):
    """ 销售大信息列表 """
    form = SalesDataModelForm()  # 引入表模板
    search_bar = SearchBar(request, form)  # 新建搜索框组件对象
    queryset = models.SalesData.objects.filter(**search_bar.filter()).order_by("-id")
    page_obj = Pagination(request, queryset, "page", 12)  # 新建翻页组件对象
    del_obj = FormBtnDelete("/salesdata/delete")  # 新建删除框组件对象
    upload_obj = FormBtnUpload("/salesdata/addform")  # 新建excel批量上传框组件对象
    context = {
        # 搜索框组件
        "search_html": search_bar.html(),
        "search_js": search_bar.js(),
        # 删除框组件
        "delete_Modal": del_obj.html_modal(),
        "delete_js": del_obj.js(),
        # excel批量上传框组件
        "upload_Modal": upload_obj.html_modal(),
        "upload_js": upload_obj.js(),
        # 翻页组件
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html(),  # html页码
    }
    return render(request, "salesdata_list.html", context)


def salesdata_add(request):
    return None


def salesdata_edit(request):
    return None


def salesdata_delete(request):
    """ 删除销售数据 """
    uid = request.GET.get("uid")
    if not models.SalesData.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.SalesData.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def salesdata_addform(request):
    """ 批量上传（excel文件） """
    from openpyxl import load_workbook
    # 1.获取用户上传的文件对象
    file_obj = request.FILES.get("upload_file")
    if file_obj:
        # 2.对象传递给openpyxl，又openpyxl读取文件的内容
        wb = load_workbook(file_obj)
        sheet = wb.worksheets[0]
        # 3.循环获取每一行数据
        for row in sheet.iter_rows(min_row=2):
            date_dict = {}
            date_dict['date'] = row[0].value
            date_dict['order_number'] = row[1].value
            date_dict['client_company'] = row[2].value
            date_dict['k3'] = row[4].value
            date_dict['product_name'] = row[5].value
            date_dict['product_specification'] = row[6].value
            date_dict['sales_volume'] = row[8].value
            date_dict['department'] = row[10].value
            date_dict['salesperson'] = row[11].value
            date_dict['gross_unit_price'] = row[12].value
            # 销售金额（元）= 实发数量 * 销售单价(元/Kg）
            date_dict['net_unit_price'] = row[14].value
            # 未税金额（元）= 实发数量 * 不含税单价（元/Kg）
            date_dict['actual_client_company'] = row[16].value
            date_dict['supply_company'] = row[18].value
            date_dict['intra_group_or_external_sales'] = row[19].value
            date_dict['product_domain_groups'] = row[21].value
            date_dict['business_trade_categories'] = row[22].value
            date_dict['new_and_returning_customers'] = row[23].value
            date_dict['product_category'] = row[30].value
            date_dict['core_product'] = row[31].value
            date_dict['order_type'] = row[32].value
            print(date_dict)
            models.SalesData.objects.create(**date_dict)
        # time.sleep(2)
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error":"上传文件有误"})