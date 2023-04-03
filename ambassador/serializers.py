from rest_framework import serializers
from core.models import Product, Link, OrderItems, Order, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

