"""
定义一些数据表，这会在数据库生成数据表，并通过DOM连接协同工作
"""

from django.db import models


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门 """
    name = models.CharField(verbose_name="部门名称", max_length=16)

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    """ 用户 """
    name = models.CharField(verbose_name="名称", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.SmallIntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)  # 整数位8(10-2)，小数位2
    create_time = models.DateField(verbose_name="入职时间")
    # 在django中做的约束
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # 2. django自动
    #   - 写的depart
    #   - 生成mysql的数据列 depart_id
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    # 【models.ForeignKey】是 Django ORM 提供的外键字段类型，用于建立两个模型之间的一对多关系。
    # 【to="Department"】指定外键关联的数据表。【to_field="id"】指定外键关联 Department 模型中的哪一个字段。
    # 【null=True, blank=True】表示在 Django 的表单验证中，这个字段可以留空。
    # 【on_delete=
    # models.SET_NULL: 指定当关联的 Department 记录被删除时，depart 字段的值会被设置为 NULL，而不是删除这条记录或抛出错误。
    # models.CASCADE: 关联对象删除时，当前对象也会被删除。
    # models.PROTECT: 阻止删除关联对象，抛出 ProtectedError。
    # models.SET_DEFAULT: 将字段设置为默认值。
    # 】
    # insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id) values("chi",123456,18,200,"2023-04-03",1,1);


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)  # 用char原因是后面方便正则表达式搜索，如果用int还得转str
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choices = {
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    }
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)
    status_choices = {
        (1, "未占用"),
        (2, "已占用"),
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "一般"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    tittle = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="任务详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", to_field="id", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    tittle = models.CharField(verbose_name="名称", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)  # 整数位8(10-2)，小数位2
    status_choices = {
        (1, "待支付"),
        (2, "已支付"),
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # 数据库的真键是：admin_id，值是储存admin的数据表中的行id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class SalesTeam(models.Model):
    """ 销售团队 """
    name = models.CharField(verbose_name="销售团队名称", max_length=64)
    business_area = models.CharField(verbose_name="业务区域", max_length=64, null=True, blank=True)
    business_segment = models.CharField(verbose_name="业务板块描述", max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Salesperson(models.Model):
    """ 销售人员 """
    team = models.ForeignKey(verbose_name="团队", to="SalesTeam", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    status_choices = {
        (1, "组员"),
        (2, "经理"),
    }
    status = models.SmallIntegerField(verbose_name="级别", choices=status_choices, default=1)
    name = models.CharField(verbose_name="销售人员姓名", max_length=64)

    def __str__(self):
        return self.name


class SalesIndicator(models.Model):
    """ 个人业绩状况 """
    name = models.ForeignKey(verbose_name="成员", to="Salesperson", to_field="id", on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name="年份")
    target_sales_volume_1 = models.IntegerField(verbose_name="1月销量指标(Kg)", default=0)
    target_sales_volume_2 = models.IntegerField(verbose_name="2月销量指标(Kg)", default=0)
    target_sales_volume_3 = models.IntegerField(verbose_name="3月销量指标(Kg)", default=0)
    target_sales_volume_4 = models.IntegerField(verbose_name="4月销量指标(Kg)", default=0)
    target_sales_volume_5 = models.IntegerField(verbose_name="5月销量指标(Kg)", default=0)
    target_sales_volume_6 = models.IntegerField(verbose_name="6月销量指标(Kg)", default=0)
    target_sales_volume_7 = models.IntegerField(verbose_name="7月销量指标(Kg)", default=0)
    target_sales_volume_8 = models.IntegerField(verbose_name="8月销量指标(Kg)", default=0)
    target_sales_volume_9 = models.IntegerField(verbose_name="9月销量指标(Kg)", default=0)
    target_sales_volume_10 = models.IntegerField(verbose_name="10月销量指标(Kg)", default=0)
    target_sales_volume_11 = models.IntegerField(verbose_name="11月销量指标(Kg)", default=0)
    target_sales_volume_12 = models.IntegerField(verbose_name="12月销量指标(Kg)", default=0)
    target_sales_revenue_1 = models.IntegerField(verbose_name="1月销售额指标(元)", default=0)
    target_sales_revenue_2 = models.IntegerField(verbose_name="2月销售额指标(元)", default=0)
    target_sales_revenue_3 = models.IntegerField(verbose_name="3月销售额指标(元)", default=0)
    target_sales_revenue_4 = models.IntegerField(verbose_name="4月销售额指标(元)", default=0)
    target_sales_revenue_5 = models.IntegerField(verbose_name="5月销售额指标(元)", default=0)
    target_sales_revenue_6 = models.IntegerField(verbose_name="6月销售额指标(元)", default=0)
    target_sales_revenue_7 = models.IntegerField(verbose_name="7月销售额指标(元)", default=0)
    target_sales_revenue_8 = models.IntegerField(verbose_name="8月销售额指标(元)", default=0)
    target_sales_revenue_9 = models.IntegerField(verbose_name="9月销售额指标(元)", default=0)
    target_sales_revenue_10 = models.IntegerField(verbose_name="10月销售额指标(元)", default=0)
    target_sales_revenue_11 = models.IntegerField(verbose_name="11月销售额指标(元)", default=0)
    target_sales_revenue_12 = models.IntegerField(verbose_name="12月销售额指标(元)", default=0)

    def __str__(self):
        return self.name


class SalesProduct(models.Model):
    """ 客户产品数据 """
    intra_or_external_sales = models.CharField(verbose_name="客户类型(内外销)", max_length=64)
    supply_company = models.CharField(verbose_name="供货基地", max_length=64)
    salesperson = models.CharField(verbose_name="业务员", max_length=64)
    product_domain_groups = models.CharField(verbose_name="组别（电子电气、家电、汽配、卫浴、内销、原料销售、国内营销、国际营销、精密组件）", max_length=64)
    initial_transaction_date = models.DateField(verbose_name="初始交易日期")
    # 新旧项目：用"初始交易日期"，以今年1月1日为分界线来判断，
    actual_client_company = models.CharField(verbose_name="客户全称", max_length=64)
    k3 = models.CharField(verbose_name="K3", max_length=64)
    product_name = models.CharField(verbose_name="材料名称", max_length=64)
    product_category = models.CharField(verbose_name="产品线", max_length=64, null=True, blank=True)
    core_product = models.CharField(verbose_name="主打产品", max_length=64, null=True, blank=True)


class SalesData(models.Model):
    """ 销售数据 """
    date = models.DateField(verbose_name="日期")
    k3 = models.CharField(verbose_name="K3", max_length=64)
    sales_volume = models.IntegerField(verbose_name="实发数量(Kg)")
    net_unit_price = models.DecimalField(verbose_name="不含税单价(元/Kg)", max_digits=27, decimal_places=14, default=0)  # 验证：销售单价(元/Kg）/ 1.13
    # 未税金额（元）= 实发数量 * 不含税单价（元/Kg）
    client_company = models.CharField(verbose_name="实际购货公司", max_length=64)
