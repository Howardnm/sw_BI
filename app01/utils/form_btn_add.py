"""
自定义的模态框--添加，使用方法：
# 在视图函数中：
    def salesdata_add(request):
    form = SalesDataModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})  # 直接传入dict，django会自动转json
    return JsonResponse({"status": False, "error": form.errors})

# 在HTML页面中：（依赖jquery）
    # 1、模态框弹窗激活按钮
    <a class="btn btn-primary" id="btnAddBar"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>添加销售信息</a>
    # 2、模态框弹窗组件，放在html_body随意一个位置
    {{ add_Modal }}
    # 3、导入模态框的js
    {% block js %}
        {{ add_js }}
    {% endblock %}

"""

from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe


class FormBtnAdd:
    def __init__(self, request, form, add_post_url, modal_tittle):
        """
        属性：
        :param request: 请求的对象
        :param form: modelform的对象
        :param add_post_url: 提交表单的url
        :param modal_tittle: 模态框标题
        """
        self.request = request
        self.form = form
        self.add_post_url = add_post_url
        self.modal_tittle = modal_tittle

    def html_modal(self):
        """ 添加数据-模态框 """
        csrf_token = get_token(self.request)  # 获取 CSRF 令牌
        page = f"""
            <!-- 新建/编辑 对话框 -->
            <div class="modal fade" id="myModal_Add" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <h4 class="modal-title">{self.modal_tittle}</h4>
                        </div>
                        <div class="modal-body">
                            <form id="formAdd" novalidate><!-- novalidate取消网页端验证，交给Django处理 -->
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
                            <button id="btnAddSave" type="button" class="btn btn-primary">保 存</button>
                        </div>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
       """
        page_string = mark_safe(page)  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string

    def js(self):
        page_str_list = []
        page = f"""
            <script type="text/javascript">
                $(function () {{
                    bindBtnAddBarEvent();
                    bindBtnAddSaveEvent();
                }})
        
                // 弹出新建的对话框
                function bindBtnAddBarEvent() {{
                    $("#btnAddBar").click(function () {{
                        // 清空对话框中的数据
                        $("#formAdd")[0].reset();
                        // 点击新建按钮，显示对话框
                        $("#myModal_Add").modal("show");
                    }});
                }}
        
                // 新建对话框的保存按钮
                function bindBtnAddSaveEvent() {{
                    $("#btnAddSave").click(function () {{
                        $(".add-error-msg").empty();  // 每次点击时先清空错误信息
                        $.ajax({{
                            url: "{self.add_post_url}",
                            type: "post",
                            data: $("#formAdd").serialize(),// serialize()是URL序列化表单字典
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
                                                var $field = $("#myModal_Add").find("#id_" + k);  // 确保只选当前模态框里的字段
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
