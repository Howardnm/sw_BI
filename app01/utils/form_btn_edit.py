"""
自定义的模态框--编辑，使用方法：
# 在视图函数中：
    def salesdata_edit(request):  # 编辑信息
        uid = request.GET.get("uid")
        obj = models.SalesData.objects.filter(id=uid).first()
        if not obj:
            return JsonResponse({"status": False, "tips": "无法编辑，该行数据不存在，请刷新重试"})
        form = SalesDataModelForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": form.errors})

    def salesdata_edit_detail(request):  # 获取要编辑的数据
        uid = request.GET.get("uid")
        obj_dict = models.SalesData.objects.filter(id=uid).values().first()  # 获得的是一个字典
        if not obj_dict:
            return JsonResponse({"status": False, "error": "数据不存在"})
        data_dict = {
            "status": True,
            "data": obj_dict
        }
        return JsonResponse(data_dict)

# 在HTML页面中：（依赖jquery）
    # 1、模态框弹窗激活按钮
        {% for obj in queryset %}
            <tr uid="{{ obj.id }}">
                <td>
                    <input uid="{{ obj.id }}" type="button" class="btn btn-xs btn-primary btn-edit" value="编辑">
                </td>
            </tr>
        {% endfor %}
    # 2、模态框弹窗组件，放在html_body随意一个位置
    {{ edit_Modal }}
    # 3、导入模态框的js
    {% block js %}
        {{ edit_js }}
    {% endblock %}
"""

from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe


class FormBtnEdit:
    def __init__(self, request, form, edit_get_detail_url, edit_post_url, modal_tittle):
        """
        属性：
        :param request: 请求的对象
        :param form: modelform的对象
        :param edit_get_detail_url: 数据请求接口
        :param edit_post_url: 提交表单的url
        :param modal_tittle: 模态框标题
        """
        self.request = request
        self.form = form
        self.edit_get_detail_url = edit_get_detail_url
        self.edit_post_url = edit_post_url
        self.modal_tittle = modal_tittle

    def html_modal(self):
        """ 编辑数据-模态框 """
        csrf_token = get_token(self.request)  # 获取 CSRF 令牌
        page = f"""
            <!-- 编辑 对话框 -->
            <div class="modal fade" id="myModal_Edit" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <h4 class="modal-title">{self.modal_tittle}</h4>
                        </div>
                        <div class="modal-body">
                            <form id="formEdit" novalidate><!-- novalidate取消网页端验证，交给Django处理 -->
                                <div class="clearfix">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                                    {"".join([
                                        f'<div class="col-xs-6">'
                                        f'<div class="form-group" style="position: relative;margin-bottom: 20px"><!-- 添加css相对定位 -->'
                                        f'<label>{field.label}</label>'
                                        f'{field}'
                                        f'<span style="color: red;position: absolute" class="add-error-msg">{field.errors[0] if field.errors else ""}</span></div></div>'
                                        for field in self.form
                                    ])}
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                            <button id="btnEditSave" type="button" class="btn btn-primary">保 存</button>
                        </div>
                    </div>
                </div>
            </div>
       """
        page_string = mark_safe(page)  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string

    def js(self):
        page_str_list = []
        page = f"""
            <script type="text/javascript">
                var EDIT_ID;
                $(function () {{
                    bindBtnEditBarEvent();
                    bindBtnEditSaveEvent();
                }})
        
                // 弹出编辑的对话框
                function bindBtnEditBarEvent() {{
                    $(".btn-edit").click(function () {{
                        // 清空对话框中的数据
                        $("#formEdit")[0].reset();
                        var uid = $(this).attr("uid");  // 获取当前行的uid
                        EDIT_ID = uid;
                        
                        // 发送Ajax去后端获取当前行的相关数据
                        $.ajax({{
                            url: "{self.edit_get_detail_url}",
                            type: "get",
                            data: {{
                                uid: uid,
                            }},
                            dataType: "JSON",
                            success: function (res) {{
                                if (res.status) {{
                                    // 将数据赋值到对话框中的标签。
                                    $.each(res.data, function (k, v) {{
                                        var $field = $("#myModal_Edit").find("#id_" + k);  // 确保只选当前模态框里的字段

                                        if ($field.is("select")) {{
                                            $field.val(v).trigger("change");
                                        }} else if ($field.is(":checkbox")) {{
                                            $field.prop("checked", v);
                                        }} else {{
                                            $field.val(v);
                                        }}
                                    }});
                                    $("#myModal_Edit").modal("show");
                                }} else {{
                                    alert(res.error);
                                }}
                            }}
                        }});
                    }});
                }}
        
                // 编辑对话框的保存按钮
                function bindBtnEditSaveEvent() {{
                    $("#btnEditSave").click(function () {{
                        $(".edit-error-msg").empty();  // 每次点击时先清空错误信息
                        $.ajax({{
                            url: "{self.edit_post_url}?uid=" + EDIT_ID,
                            type: "post",
                            data: $("#formEdit").serialize(),// serialize()是URL序列化表单字典
                            dataType: "JSON",  // 把服务器返回的HttpResponse的JSON字符串识别为对象，方便调用，如果服务器用django的JsonResponse返回，就不需要声明dataType: "JSON"
                            success: function (res) {{  // {{"status": False, "error": form.errors}}
                                if (res.status) {{
                                    location.reload();// 用JS实现页面的刷新
                                }} else {{
                                    if (res.tips) {{
                                        alert(res.tips);
                                    }} else {{
                                        // 把错误信息显示在对话框中。
                                        $.each(  // 循环res.error字典
                                            res.error, function (k, v) {{
                                                var $field = $("#myModal_Edit").find("#id_" + k);  // 确保只选当前模态框里的字段
                                                $field.next().text(v[0]);  // $("#id_" + k)是input框的id，该id的class标签是modelform自动写上去的。next()指的是input标签的下一个标签，即<span>
                                            }}
                                        )
                                    }}
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
