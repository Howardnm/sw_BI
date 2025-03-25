"""
自定义的模态框--添加，使用方法：
# 在视图函数中：

# 在HTML页面中：（依赖jquery）
    # 1、模态框弹窗激活按钮
    <a class="btn btn-primary" id="btn-delete-all"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>一键删除所有销售数据</a>
    # 2、模态框弹窗组件，放在html_body随意一个位置
    {{ delete_all_Modal }}
    # 3、导入模态框的js
    {% block js %}
        {{ delete_all_js }}
    {% endblock %}

"""

from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe


class FormBtnDelAll:
    def __init__(self, request, post_url, label, delete_tips="将会删除所有数据，请谨慎操作！！！"):
        """
        属性：
        :param request: 请求的对象
        :param post_url: 提交表单的url
        :param delete_tips: 模态框提示语
        """
        self.request = request
        self.post_url = post_url
        self.label = label
        self.delete_tips = delete_tips

    def html_modal(self):
        """ 添加数据-模态框 """
        csrf_token = get_token(self.request)  # 获取 CSRF 令牌
        page = f"""
            <div class="modal fade" id="deleteAllModal" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                    <div class="alert alert-danger alert-dismissible fade in" role="alert">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
                        <h4>是否确定删除？</h4>
                        <p style="margin-bottom: 10px">{self.delete_tips}</p>
                        <form id="formDelAll" novalidate><!-- novalidate取消网页端验证，交给Django处理 -->
                            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                            <label>{self.label}</label>
                            <input type="password" name="pwd">
                            <span style="color: red;position: absolute" class="delAll-error-msg"></span>
                        </form>
                        <p style="text-align: right">
                            <button id="btnConfirmDelAll" type="button" class="btn btn-danger">确 定</button>
                            <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                        </p>
                    </div>
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
                    bindBtnDelAllBarEvent();
                    bindBtnDelAllEvent();
                }})
        
                // 弹出模态框
                function bindBtnDelAllBarEvent() {{
                    $("#btn-delete-all").click(function () {{
                        // 清空对话框中的数据
                        $("#formDelAll")[0].reset();
                        // 点击新建按钮，显示对话框
                        $("#deleteAllModal").modal("show");
                    }});
                }}
        
                // 模态框框的保存按钮
                function bindBtnDelAllEvent() {{
                    $("#btnConfirmDelAll").click(function () {{
                        $(".delAll-error-msg").empty();  // 每次点击时先清空错误信息
                        $.ajax({{
                            url: "{self.post_url}",
                            type: "post",
                            data: $("#formDelAll").serialize(),// serialize()是URL序列化表单字典
                            dataType: "JSON",  // 把服务器返回的HttpResponse的JSON字符串识别为对象，方便调用，如果服务器用django的JsonResponse返回，就不需要声明dataType: "JSON"
                            success: function (res) {{  // {{"status": False, "error": form.errors}}
                                if (res.status) {{
                                    location.reload();// 用JS实现页面的刷新
                                }} else {{
                                    $(".delAll-error-msg").text(res.error);
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
