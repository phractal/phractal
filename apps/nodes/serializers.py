import time
from rest_framework import serializers

from nodes.models import Node
from nodes.models import TaskNode
from wallets.models import MyAccount


class NodeSerializers(serializers.ModelSerializer):
    succeed_tasks = serializers.SerializerMethodField(label="完成任务数", read_only=True)
    failed_tasks = serializers.SerializerMethodField(label="失败任务数", read_only=True)
    total_revenue = serializers.SerializerMethodField(label="总收益", read_only=True)

    class Meta:
        model = Node
        fields = "__all__"
        ordering = ["id"]
        depth = 2

    def get_succeed_tasks(self, obj):
        succeed_tasks = TaskNode.objects.filter(node=obj, status=3).count()
        return succeed_tasks

    def get_failed_tasks(self, obj):
        failed_tasks = TaskNode.objects.filter(node=obj, status=2).count()
        return failed_tasks

    def get_total_revenue(self, obj):
        profit_nodes = TaskNode.objects.filter(node=obj, status=3).all()  # 找到该节点所有完成的任务 计算完成任务时间 从而获得总收益, 注意对应的时间格式
        total_revenue = sum([self._calculate_total_revenue(node=node) for node in profit_nodes])
        return total_revenue

    def _calculate_total_revenue(self, node):
        if node.that_time_unit_price_symbol == "ps":
            total_revenue = round(
                (self.convert_timestamp(node.end_time) - self.convert_timestamp(node.start_time)) * float(
                    node.that_time_unit_price), 2)
            return total_revenue
        if node.that_time_unit_price_symbol == "pt":
            total_revenue = round(node.that_time_unit_price, 2)
            return total_revenue
        if node.that_time_unit_price_symbol == "ph":
            total_revenue = round(
                (self.convert_timestamp(node.end_time) - self.convert_timestamp(node.start_time)) / 3600 * float(
                    node.that_time_unit_price), 2)
            return total_revenue

    @staticmethod
    def convert_timestamp(datetime):
        return int(round(time.mktime(datetime.timetuple())))

class TaskNodeSerializers(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    this_time_revenue = serializers.SerializerMethodField(label="本次节点收益", read_only=True)
    node_detail = serializers.SerializerMethodField(label="节点详情", read_only=True)

    class Meta:
        model = TaskNode
        fields = "__all__"

    def create(self, validated_data):
        task = validated_data.get("task")
        if task.status != 1:
            return serializers.ValidationError("该任务已经完成或者失败")
        if validated_data.get("get_status_display", None):
            del validated_data["get_status_display"]
        price = validated_data["node"].unit_price
        validated_data["that_time_unit_price"] = price

        return TaskNode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        status = validated_data.get("get_status_display", "")
        if status:
            instance.status = int(validated_data["get_status_display"])
        instance.task = validated_data.get("task", instance.task)
        instance.node = validated_data.get("node", instance.node)
        instance.that_time_unit_price = validated_data.get("that_time_unit_price", instance.that_time_unit_price)
        instance.that_time_unit_price_symbol = validated_data.get("that_time_unit_price_symbol",
                                                                  instance.that_time_unit_price_symbol)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.save()
        return instance

    def get_node_detail(self, obj):
        serializer = NodeSerializers(obj.node)
        return serializer.data

    # def get_this_time_revenue(self, obj):
    #     '''
    #     当时间为初始时间和开始时间的时候用此函数
    #     :param obj:
    #     :return:
    #     '''
    #     if not obj.end_time:
    #         return 0.00
    #     if obj.that_time_unit_price_symbol == "ps":
    #         this_time_revenue = round(
    #             (self.convert_timestamp(obj.end_time) - self.convert_timestamp(obj.start_time)) * float(
    #                 obj.that_time_unit_price), 2)
    #         return this_time_revenue
    #     if obj.that_time_unit_price_symbol == "pt":
    #         this_time_revenue = round(obj.that_time_unit_price, 2)
    #         return this_time_revenue
    #     if obj.that_time_unit_price_symbol == "ph":
    #         this_time_revenue = round(
    #             (self.convert_timestamp(obj.end_time) - self.convert_timestamp(obj.start_time)) / 3600 * float(
    #                 obj.that_time_unit_price), 2)
    #         return this_time_revenue

    def get_this_time_revenue(self, obj):
        '''
        获取每个节点单次运行的时间
        :param obj:
        :return:
        '''
        if obj.that_time_unit_price_symbol == "ps":
            this_time_revenue = round(float(obj.use_time) * float(obj.that_time_unit_price), 2)
            return this_time_revenue
        if obj.that_time_unit_price_symbol == "pt":
            this_time_revenue = round(obj.that_time_unit_price, 2)
            return this_time_revenue
        if obj.that_time_unit_price_symbol == "ph":
            this_time_revenue = round(float(obj.use_time) / 3600 * float(obj.that_time_unit_price), 2)
            return this_time_revenue

    @staticmethod
    def convert_timestamp(datetime):
        return int(round(time.mktime(datetime.timetuple())))
