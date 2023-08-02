from rest_framework.generics import RetrieveAPIView

from order.models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    product = OrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        request = self.context.get('request')
        user = request.user
        total_sum = 0

        for product in products:
            try:
                total_sum += product['quantity'] * product['product']
            except:
                total_sum += product['product'].price

        order = Order.objects.create(user=user, status='in_process', total_sum=total_sum, **validated_data)

        for product in products:
            try:
                OrderItem.objects.create(order=order,
                                         product=product['product'],
                                         quantity=product['product'].quantity)

            except:
                    OrderItem.objects.create(order=order,
                                             product=product['product'])

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = OrderItemSerializer(
            instance.items.all(), many=True
        ).data
        return representation


