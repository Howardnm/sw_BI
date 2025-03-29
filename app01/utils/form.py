"""
定义一些form表单，负责管理form表单允许填写什么内容，填写内容的规范化格式
作用于：登录、增、改功能。用于login.html、add.html、edit.html页面
"""

from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.encrypt import md5
from django.contrib.auth.hashers import make_password, check_password


# 1、Form自定义方法
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True  # 必填
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )


# 2、ModelForm方法(推荐)
class LoginModelForm(BootStrapModelForm):
    code = forms.CharField(
        label="图片验证码",
        widget=forms.TextInput,
        required=True
    )  # 用于输入验证码

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean(self):
        """ 先验证验证码，再验证用户名和密码 """
        cleaned_data = super().clean()
        # cleaned_data = {'username': 'admin', 'password': 'qwe', 'code': '1234'}  # 用户填入的表单内容
        # 1 **先检查验证码**
        input_code = cleaned_data.get("code", "")
        session_code = self.request.session.get("image_code")
        if not session_code:
            self.add_error("code", "验证码已过期")
            return  # **返回，跳过用户名和密码验证**
        if input_code.strip().lower() != session_code.lower():  # 统一小写进行比对
            self.add_error("code", "验证码错误")
            return  # **返回，跳过用户名和密码验证**

        # 2 **再检查用户名和密码**
        user_name = cleaned_data.get("username")
        pwd = cleaned_data.get("password")
        if pwd:
            pwd = md5(pwd)
            cleaned_data["password"] = pwd
        obj = models.Admin.objects.filter(username=user_name, password=pwd).first()
        if not obj:
            self.add_error("password", "用户名或密码错误")
        else:
            self.instance = obj  # 把用户信息对象导入到 form.instance ，可在 views.py 中，通过form.instance获取用户信息对象
        return cleaned_data


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput  # forms.PasswordInput(render_value=True)作用：用户输入完密码如果错误，跳转页面时不会清空输入框
    )  # 用于再次输入密码校验

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean(self):
        """钩子方法（用于验证传入表单的数据）"""
        cleaned_data = super().clean()
        # 直接使用 self.cleaned_data["password"]，如果 password 先前的验证失败（比如为空），会导致 KeyError。
        # get() 方法 如果字段不存在，返回 None，不会引发 KeyError。
        user_name = cleaned_data.get("username")
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        # 只有当 password 和 confirm_password 都有效时，才进行匹配。避免 None != None 的情况导致不必要的错误。
        # self.add_error("password2", "两次输入的密码不一致") 不会立即抛出异常，但会将错误存入 self.errors。
        # form.is_valid() 在检查 self.errors 时，如果有错误，则返回 False，阻止表单提交。
        exists: bool = models.Admin.objects.exclude(id=self.instance.pk).filter(username=user_name).exists()
        if exists:
            self.add_error("username", "用户名已存在！")
        if pwd and confirm and confirm != pwd:
            self.add_error("confirm_password", "密码不一致！")
        if pwd and confirm:
            cleaned_data["password"] = md5(pwd)
            # cleaned_data["password"] = make_password(pwd)  # 更安全的加密方式
            # 用户登录时：用 check_password() 进行密码匹配。check_password("123456", pwd)  # 匹配成功会返回true，否则false
        # 返回什么，此字段以后保存到数据库就是什么。
        return cleaned_data


class AdminEditForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]  # 只开启修改用户名的权限

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get("username")
        exists: bool = models.Admin.objects.exclude(id=self.instance.pk).filter(username=user_name).exists()
        if exists:
            self.add_error("username", "用户名已存在！")
        return cleaned_data


class AdminResetPwdModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )  # 用于再次输入密码校验

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if pwd and confirm and confirm != pwd:
            self.add_error("confirm_password", "密码不一致！")
        if pwd and confirm:
            md5_pwd = md5(pwd)
            exists: bool = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
            if exists:
                self.add_error("password", "密码不能与之前一致！")
            cleaned_data["password"] = md5_pwd
            # cleaned_data["password"] = make_password(pwd)  # 更安全的加密方式
            # 用户登录时：用 check_password() 进行密码匹配。check_password("123456", pwd)  # 匹配成功会返回true，否则false
        return cleaned_data


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.Userinfo  # 导入Userinfo数据库模型
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误"), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = "__all__"  # 所有字段
        # exclude = ['level']  # 排除该字段

    # # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data.get("mobile")
        # 当页面是编辑模式时，当前编辑的ID是 self.instance.pk（添加模式时，该值为None）。也可以用self.instance.id，但 primary_key 如果不是 "id" 那就出错，"pk" 一定是指向 primary_key。
        # 验证手机号是否重复
        exists: bool = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 禁用字段方法1
    # mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = "__all__"  # 所有字段
        # 禁用字段方法2
        # exclude = ['mobile']  # 排除该字段


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput  # 自定义输入框样式
        }


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["oid", "admin"]  # 排除不想显示的数据列


class SalesTeamModelForm(BootStrapModelForm):
    class Meta:
        model = models.SalesTeam
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name:
            exists: bool = models.SalesTeam.objects.exclude(id=self.instance.pk).filter(name=name).exists()
            if exists:
                self.add_error("name", "团队名称已存在！")
        return cleaned_data


class SalespersonModelForm(BootStrapModelForm):
    class Meta:
        model = models.Salesperson
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name:
            exists: bool = models.Salesperson.objects.exclude(id=self.instance.pk).filter(name=name).exists()
            if exists:
                self.add_error("name", "该人员已存在！")
        return cleaned_data


class SalesIndicatorModelForm(BootStrapModelForm):
    class Meta:
        model = models.SalesIndicator
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        year = cleaned_data.get("year")
        if name and year:
            exists: bool = models.SalesIndicator.objects.exclude(id=self.instance.pk).filter(name=name, year=year).exists()
            if exists:
                self.add_error("year", f"{name}, {year}年份数据已存在！若需更新数据，请删除该数据，然后重新导入！")
        return cleaned_data


class SalesProductModelForm(BootStrapModelForm):
    class Meta:
        model = models.SalesProduct
        fields = "__all__"


class SalesDataModelForm(BootStrapModelForm):
    class Meta:
        model = models.SalesData
        fields = "__all__"
