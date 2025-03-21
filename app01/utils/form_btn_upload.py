from django.utils.safestring import mark_safe


class FormBtnUpload:

    def __init__(self, upload_post_url):
        self.upload_post_url = upload_post_url

    def html_modal(self):
        """
        批量上传 对话框
        """
        page_str_list = []
        page = """
            <div class="modal fade" id="myModal_uploadBar" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
                            <h4 class="modal-title">Excel批量上传</h4>
                        </div>
                        <form id="formUploadFile" enctype="multipart/form-data" novalidate>
                            {% csrf_token %}
                            <div class="form-group">
                                <input type="file" name="upload_file">
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                                <button id="btnUpload" class="btn btn-primary">上 传</button>
                            </div>
                        </form>
                    </div><!-- /.modal-content -->
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
                $(function () {{
                    bindBtnUploadBarEvent();
                    bindBtnUploadSaveEvent();
                }})
        
                // 弹出对话框
                function bindBtnUploadBarEvent() {{
                    $("#btnUploadBar").click(function () {{
                        // 点击该按钮，显示对话框
                        $("#myModal_uploadBar").modal("show");
                    }});
                }}
        
                // 批量上传的对话框的保存按钮
                function bindBtnUploadSaveEvent() {{
                    $("#btnUpload").click(function () {{
                        event.preventDefault();  // 阻止表单的默认提交行为

                        var originalText = $(this).text();  // 保存原始按钮文字
                        var originalClass = $(this).attr("class");  // 保存原始 class
                        $(this).text('导入中...');  // 更改按钮文字
                        $(this).removeClass("btn-primary").addClass("btn-warning");  // 修改按钮样式为“警告”按钮
                        
                        var formData = new FormData($("#formUploadFile")[0]); // 获取表单数据
                        $.ajax({{
                            url: "{self.upload_post_url}",
                            type: "post",
                            data: formData,
                            processData: false,  // 不处理数据，让 FormData 以二进制形式传输
                            contentType: false,  // 让浏览器自动设置 Content-Type
                            success: function (res) {{  // {{"status": False, "error": form.errors}}
                                console.log(res);
                                if (res.status) {{
                                    location.reload();
                                }} else {{
                                    alert(res.error);  // 删除失败
                                }}
                            }},
                            complete: function () {{
                                $("#btnUpload").text(originalText);  // 恢复原始按钮文字
                                $("#btnUpload").attr("class", originalClass);  // 恢复原始 class
                            }}
                        }});
                    }});
                }}
            </script>
        """
        page_str_list.append(page)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string
