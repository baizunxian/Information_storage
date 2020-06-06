from django.db import models

# Create your models here.


class Base(models.Model):
    class Meta:
        abstract = True
        verbose_name = '公共字段'
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class User(Base):
    number = models.CharField(max_length=100, verbose_name='编号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    pwd = models.CharField(max_length=100, verbose_name='密码')
    phoneNumber = models.CharField(max_length=100, verbose_name='手机号码', null=True)
    sex = models.CharField(max_length=2, verbose_name='性别')  # 0 女 1 男
    age = models.CharField(max_length=100, verbose_name='年龄', null=True)
    college = models.CharField(max_length=100, verbose_name='学院', null=True)
    major = models.CharField(max_length=100, verbose_name='专业', null=True)
    sclass = models.CharField(max_length=100, verbose_name='班级', null=True)
    type = models.IntegerField(verbose_name='用户类型', default=1)  # 0 laos 1 学生


class Storage(Base):
    storage_text = models.TextField(verbose_name='存证文本', null=True)
    state = models.IntegerField(verbose_name='申请状态', default=0)  # 0未审核 ，1审核通过， 2审核不通过
    storage_img = models.FileField(verbose_name='申请状态', upload_to='img', null=True)
    storage_img_name = models.CharField(max_length=255, verbose_name='图片名', null=True)
    remark = models.CharField(max_length=255, verbose_name='备注')
    user_name = models.CharField(max_length=255, verbose_name='用户名')
    user_number = models.CharField(max_length=255, verbose_name='学号')
    approve_time = models.DateTimeField(verbose_name='审批时间', null=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='申请用户', null=True)

