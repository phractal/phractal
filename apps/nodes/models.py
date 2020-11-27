from _datetime import datetime
from django.conf import settings
from django.db import models
from tasks.models import Task

User = settings.AUTH_USER_MODEL


class Node(models.Model):
    PRICE_CHOICE = (
        ("ps", "per_second"),
        ("pt", "per_time"),
        ("ph", "per_hour"),
    )
    name = models.CharField("节点名称", max_length=64)
    node_id = models.CharField("节点ID", max_length=16)
    ip = models.CharField("节点IP", max_length=16)

    path = models.CharField("存储路径", max_length=255)

    category = models.CharField("节点类型", max_length=16, default="搜索节点")

    state = models.CharField("节点状态", max_length=32, default="close")

    create_time = models.DateTimeField("节点创建时间", auto_now_add=True)
    unit_price = models.DecimalField("节点单价", max_digits=6, decimal_places=2, default=0.01)
    unit_price_symbol = models.CharField("节点价格类型", default="ps", choices=PRICE_CHOICE, max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField("维度", max_digits=15, decimal_places=5, null=True)
    longitude = models.DecimalField("经度", max_digits=15, decimal_places=5, null=True)
    update_time = models.DateTimeField("节点更新时间", auto_now_add=True)
    class Meta:
        verbose_name = "节点"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.name


class TaskNode(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    node = models.ForeignKey(Node, on_delete=models.DO_NOTHING)
    status = models.IntegerField(default=1, choices=((1, "执行"), (2, "失败"), (3, "成功")))
    that_time_unit_price = models.DecimalField("当时节点单价", max_digits=6, decimal_places=2, null=True)
    that_time_unit_price_symbol = models.CharField("当时节点单价类型", max_length=8, default="ps")
    start_time = models.DateTimeField("任务执行开始时间", auto_now_add=True)
    end_time = models.DateTimeField("任务执行结束时间", null=True)
    use_time = models.CharField("任务执行消耗时间", max_length=32, null=True)

    class Meta:
        verbose_name = "任务节点关联"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{datetime.now()} - {self.start_time}"


class CompressNode(models.Model):
    node_type = models.CharField(max_length=256, verbose_name='压缩包节点类型')
    node_num = models.IntegerField(verbose_name='解压次数')
    node_path = models.CharField(max_length=256, verbose_name='节点路径')

    class Meta:
        verbose_name = "节点压缩包"
        verbose_name_plural = verbose_name

class Monitor_node(models.Model):
    max_cpu = models.IntegerField(default=35,verbose_name='cpu最大使用率')
    max_memory = models.IntegerField(default=35,verbose_name='内存最大使用率')

    class Meta:
        verbose_name='系统资源配置'
        verbose_name_plural=verbose_name