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
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2,
                                  default=0)  # 整数位8(10-2)，小数位2
    create_time = models.DateField(verbose_name="入职时间")
    # 在django中做的约束
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # 2. django自动
    #   - 写的depart
    #   - 生成mysql的数据列 depart_id
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)
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

    def __str__(self):
        return self.name


class Salesperson(models.Model):
    """ 销售人员 """
    name = models.CharField(verbose_name="销售人员姓名", max_length=64)
    status_choices = {
        (1, "组员"),
        (2, "经理"),
    }
    status = models.SmallIntegerField(verbose_name="级别", choices=status_choices, default=1)
    team = models.ForeignKey(verbose_name="团队", to="SalesTeam", to_field="id", null=True, blank=True,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Performance(models.Model):
    """ 个人业绩状况 """
    name = models.ForeignKey(verbose_name="成员", to="Salesperson", to_field="id", on_delete=models.CASCADE)
    month = models.DateField(verbose_name="月份")
    target = models.IntegerField(verbose_name="当月目标量")
    target_achievement = models.IntegerField(verbose_name="当月完成量")
    sales_revenue = models.IntegerField(verbose_name="当月销售额")

    def __str__(self):
        return self.name

