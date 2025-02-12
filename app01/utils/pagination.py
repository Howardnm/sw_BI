"""
自定义的分页组件，使用方法：
# 在视图函数中：
    def pretty_list(request):
        # 1、根据需求筛选数据
        queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")
        # 2、实例化分页对象
        page_obj = Pagination(request, queryset, "page")
        # 3、
        context = {
            "queryset": page_obj.page_queryset,  # 分完页的数据
            "page_string": page_obj.html()       # html页码
        }
        return render(request, "pretty_list.html", context)

# 在HTML页面中：
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>...</th>
            </tr>
        </thead>
        <tbody>
            {% for obj in queryset %}
                <tr>
                    <th>{{ obj.id }}</th>
                    <td>{{ obj.xxx }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

    <div>
        <ul class="pagination">
            {{ page_string }}
        </ul>
    </div>

"""
from django.utils.safestring import mark_safe


class Pagination:

    def __init__(self, request, queryset, page_param="page", page_size=10, plus=2):
        """
        属性：
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/pretty/list?page=12
        :param plus: 显示当前页的前后页码按钮数量
        """

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True  # 把对象变为可变状态（Django中默认不可修改状态）
        self.query_dict = query_dict
        self.page_param = page_param

        if request.GET.get(page_param, 1):
            page = int(request.GET.get("page", 1))
            page = 1 if page <= 0 else page
        else:
            page = 1

        self.page = page
        self.page_size = page_size  # 每页显示10条数据
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        self.plus = plus
        # 数据总条数
        self.total_count = queryset.count()
        # 总页码(切片数量)
        self.total_page_count, div = divmod(self.total_count, self.page_size)
        if div:
            self.total_page_count += 1  # for循环：取前不取后，所以要补1

    def html(self):
        """
        :return: 若干个<li></li>的HTML文本的字符串
        """
        # 计算出，显示当前页的前2页，后2页
        start_page = self.page - self.plus
        end_page = self.page + self.plus + 1
        # 判断语句：避免页码显示坍缩，保持至少（2 * plus + 1）的数量。
        if start_page >= self.total_page_count - 2 * self.plus:
            start_page = self.total_page_count - 2 * self.plus
        if end_page <= 2 * self.plus + 1:
            end_page = 2 * self.plus + 1 + 1

        """ 制作html页码 """
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_param, [1])
        if self.page > 1 + self.plus:
            ele = f'<li><a href="?{self.query_dict.urlencode()}"><span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span></a></li>'
            page_str_list.append(ele)
        # 中间页码
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if 0 < i <= self.total_page_count:
                if i == self.page:
                    ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                else:
                    ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
                page_str_list.append(ele)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])

        search_string = f"""
        </ul>
        <ul class="pagination" style="width: 130px; margin-left: 30px">
            <form method="get">
                <div class="input-group">
                    <input type="number" name="page" class="form-control" placeholder="页码">
                    <span class="input-group-btn">
                        <button class="btn btn-primary" type="submit">
                            跳转
                        </button>
                    </span>
                </div>
            </form>
        """

        if self.page < self.total_page_count - self.plus:
            ele = f'<li><a href="?{self.query_dict.urlencode()}"><span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span></a></li>'
            page_str_list.append(ele)
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))  # 导入django的mark_safe模块，字符串才会写进html页面中

        return page_string
