"""
自定义的数据表搜索框，使用方法：
# 在视图函数中：
    def salesdata_list(request):
        form = SalesDataModelForm()
        search_bar = SearchBar(request, form)
        queryset = models.SalesData.objects.filter(**search_bar.filter()).order_by("-id")
        context = {
            "search_html": search_bar.html(),  # 搜索框
            "search_js": search_bar.js(),  # 搜索框
        }
        return render(request, "salesdata_list.html", context)

# 在HTML页面中：（依赖jquery）
    # 1、搜索框弹窗激活按钮
    <a class="btn btn-success" id="btnSearchBar" style="float: right"><span class="glyphicon glyphicon-search" aria-hidden="true"></span>搜 索</a>
    # 2、搜索框弹窗组件，放在html_body随意一个位置
    {{ search_html }}
    # 3、导入搜索框的js
    {% block js %}
        {{ search_js }}
    {% endblock %}

"""

from django.forms import DateField, DecimalField, IntegerField
from django.utils.safestring import mark_safe


class SearchBar:

    def __init__(self, request, modelform):
        """
        属性：
        :param request: 请求的对象
        :param modelform: modelform的对象
        """
        self.request = request
        self.modelform = modelform

    class Object:
        def __init__(self, name, label, input_type, value=""):
            """
            属性：
            :param name: 输入框的name，提交get时的key
            :param label: 输入框的标题
            :param input_type: 输入框的输入类型(text、int、date)
            :param value: 输入框的内容
            """
            self.name = name
            self.label = label
            self.type = input_type
            self.value = value

    def filter(self):
        """ 整理搜索框输入的关键字，输出一个用于数据库筛选的.filter() """
        data_dict = {}
        for field_name, field in self.modelform.fields.items():
            search_input = self.request.GET.get(f"search_{field_name}", "")  # 有值传值，没值传空
            min_value = self.request.GET.get(f"search_{field_name}_min", "")
            max_value = self.request.GET.get(f"search_{field_name}_max", "")
            if search_input or min_value or max_value:
                if isinstance(field, (DateField, DecimalField, IntegerField)):
                    # 对日期、数字字段，做范围搜索
                    min_value = self.request.GET.get(f"search_{field_name}_min", "")
                    max_value = self.request.GET.get(f"search_{field_name}_max", "")
                    if min_value:
                        data_dict[f"{field_name}__gte"] = field.to_python(min_value)
                    if max_value:
                        data_dict[f"{field_name}__lte"] = field.to_python(max_value)
                else:
                    data_dict[f"{field_name}__icontains"] = search_input  # __icontains：不分大小写搜索
        return data_dict

    def form(self):
        """ 对象化每个html_input输入框的必要信息 """
        search_form = []
        for field_name, field in self.modelform.fields.items():
            search_input = self.request.GET.get(f"search_{field_name}", "")  # 有值传值，没值传空
            if search_input:
                obj = self.Object(f"search_{field_name}", field.label, field.widget.input_type, search_input)
            else:
                obj = self.Object(f"search_{field_name}", field.label, field.widget.input_type)
            # 如果是日期字段，添加范围选择
            if isinstance(field, DateField):
                start_value = self.request.GET.get(f"search_{field_name}_min", "")
                end_value = self.request.GET.get(f"search_{field_name}_max", "")
                search_form.append(self.Object(f"search_{field_name}_min", f"开始{field.label}", "date", start_value))
                search_form.append(self.Object(f"search_{field_name}_max", f"结束{field.label}", "date", end_value))

            # 如果是数字字段，添加范围选择
            elif isinstance(field, (DecimalField, IntegerField)):
                min_value = self.request.GET.get(f"search_{field_name}_min", "")
                max_value = self.request.GET.get(f"search_{field_name}_max", "")
                search_form.append(self.Object(f"search_{field_name}_min", f"{field.label}_最小值", "number", min_value))
                search_form.append(self.Object(f"search_{field_name}_max", f"{field.label}_最大值", "number", max_value))
            else:
                search_form.append(obj)
        return search_form

    def html(self):
        """ 制作搜索框的html代码 """
        page_str_list = []

        html_string_start = """
        <!-- 删除提醒 对话框 -->
        <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="alert alert-danger alert-dismissible fade in" role="alert">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
                    <h4>是否确定删除？</h4>
                    <p style="margin-bottom: 10px">删除后，所有关联的数据都会被删除的。</p>
                    <p style="text-align: right">
                        <button id="btnConfirmDelete" type="button" class="btn btn-danger">确 定</button>
                        <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                    </p>
                </div>
            </div><!-- /.modal-dialog -->
        </div><!-- /.modal -->
        """
        page_str_list.append(html_string_start)

        for search in self.form():
            if search.type in ["date", "number"]:
                div_class = "col-xs-3"
            else:
                div_class = "col-xs-6"
            html_input = f"""
                <div class="{div_class}">
                    <label style="margin-top: 10px">{search.label}</label>
                    <input type="{search.type}" name="{search.name}" class="form-control" placeholder="{search.type}" value="{search.value}">
                </div>
            """
            page_str_list.append(html_input)

        html_string_end = """
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">取 消</button>
                                <button type="submit" class="btn btn-primary">搜 索</button>
                                <button id="btnSearchBarClear" type="button" class="btn btn-info" style="float: left;">清 空</button>
                            </div>
                        </form>
                    </div><!-- /.modal-content -->
                </div><!-- /.modal-dialog -->
            </div><!-- /.modal -->
        """
        page_str_list.append(html_string_end)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string

    def js(self):
        page_str_list = []
        page = """
            <script type="text/javascript">
                $(function () {
                    bindBtnSearchBarEvent();
                    bindBtnSearchBarClearEvent();
                })
        
                // 弹出搜索框
                function bindBtnSearchBarEvent() {
                    $("#btnSearchBar").click(function () {
                        // 点击新建按钮，显示对话框
                        $("#myModal_btnSearchBar").modal("show");
                    });
                }
        
                // 搜索框的清空按钮
                function bindBtnSearchBarClearEvent() {
                    $("#btnSearchBarClear").click(function () {
                        $("#btnSearchBar_form")[0].reset();
                        // 手动清空可能未被 reset() 清空的字段（例如 select, textarea）
                        $('#btnSearchBar_form input').val('');
                        $('#btnSearchBar_form select').val('');
                        $('#btnSearchBar_form textarea').val('');
                    });
                }
            </script>
        """
        page_str_list.append(page)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中
        return page_string
