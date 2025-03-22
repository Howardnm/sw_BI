"""
自定义的模态框--删除，使用方法：
# 在视图函数中：
    def salesdata_delete(request):
    uid = request.GET.get("uid")
    if not models.SalesData.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.SalesData.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

# 在HTML页面中：（依赖jquery）
    # 1、模态框弹窗激活按钮
        {% for obj in queryset %}
            <tr uid="{{ obj.id }}">
                <td>
                    <input uid="{{ obj.id }}" type="button" class="btn btn-xs btn-danger btn-delete" value="删除">
                </td>
            </tr>
        {% endfor %}
    # 2、模态框弹窗组件，放在html_body随意一个位置
    {{ delete_Modal }}
    # 3、导入模态框的js
    {% block js %}
        {{ delete_js }}
    {% endblock %}
"""

from django.utils.safestring import mark_safe


class FormBtnDelete:

    def __init__(self, delete_get_url, delete_tips="删除后，所有关联的数据都会被删除的。"):
        """
        属性：
        :param delete_get_url: get删除请求的url
        :param delete_tips: 模态框提示内容
        """
        self.delete_get_url = delete_get_url
        self.delete_tips = delete_tips

    def html_modal(self):
        """ 删除-模态框 """
        page_str_list = []
        page = f"""
            <!-- 删除提醒 对话框 -->
            <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                    <div class="alert alert-danger alert-dismissible fade in" role="alert">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
                        <h4>是否确定删除？</h4>
                        <p style="margin-bottom: 10px">{self.delete_tips}</p>
                        <p style="text-align: right">
                            <button id="btnConfirmDelete" type="button" class="btn btn-danger">确 定</button>
                            <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                        </p>
                    </div>
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
        """
        page_str_list.append(page)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string

    def js(self):
        page_str_list = []
        page = f"""
            <script type="text/javascript">
                var DELETE_ID;
        
                $(function () {{
                    bindBtnDeleteEvent();
                    bindBtnConfirmDeleteEvent();
                }})
        
                // 弹出删除订单提示的对话框
                function bindBtnDeleteEvent() {{
                    $(".btn-delete").click(function () {{
                        // 显示删除对话框
                        $("#deleteModal").modal("show");
                        // 获取当前行的ID并赋值给全局变量。
                        DELETE_ID = $(this).attr("uid");
        
                    }});
                }}
        
                // 删除订单提示的对话框的确定按钮
                function bindBtnConfirmDeleteEvent() {{
                    $("#btnConfirmDelete").click(function () {{
                        // 点击确认删除按钮，将全局变量中设置的那个要删除ID发送到后台。
                        $.ajax({{
                            url: "{self.delete_get_url}",  // /order/delete?uid=123
                            type: "GET",
                            data: {{
                                uid: DELETE_ID,
                            }},
                            dataType: "JSON",
                            success: function (res) {{  // {{"status": False, "error": form.errors}}
                                if (res.status) {{
                                    $("#deleteModal").modal("hide");  // 隐藏删除提示框
                                    $("tr[uid='" + DELETE_ID + "']").remove();  // 在页面上将当前一行数据删除（js，在前端实现）
                                    DELETE_ID = 0;  // 置空变量
                                    // location.reload();// 用JS实现页面的刷新（推荐，简单粗暴）
                                }} else {{
                                    alert(res.error);  // 删除失败
                                }}
                            }}
                        }});
                    }});
                }}
            </script>
        """
        page_str_list.append(page)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string
