from rest_framework import serializers
from core.models import Product, Link, OrderItems, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    # getting the total number of order items
    # this is how we add calculated field in a response which is
    # not part of the model attribute
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        ordered_items = OrderItems.objects.filter(order_id=obj.id)
        return sum(order.price * order.quantity for order in ordered_items)

    class Meta:
        model = Order
        fields = '__all__'
