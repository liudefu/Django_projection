# coding=utf-8
from rest_framework import serializers

from areas.models import Areas


# noinspection PyAbstractClass
class AreasSerializer(serializers.ModelSerializer):
    """省序列化器"""

    class Meta:
        model = Areas
        fields = ("id", "name")


# noinspection PyAbstractClass
class SubsSerializer(serializers.ModelSerializer):
    """市县序列化器"""
    areas = AreasSerializer(many=True, read_only=True)

    class Meta:
        model = Areas
        fields = ["id", "name", "areas"]
