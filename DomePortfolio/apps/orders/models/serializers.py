from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):  # noqa must implement abstract
    error = serializers.CharField()
    msg = serializers.CharField()


class CompleteOrderSerializer(serializers.Serializer):  # noqa must implement abstract
    order_id = serializers.CharField()
    grant = serializers.CharField()
