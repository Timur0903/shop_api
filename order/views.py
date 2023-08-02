from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer


# Create your views here.
class OrderAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = OrderSerializer(instance=orders, many=True)

        return Response(serializer.data, status=200)

class OrderConfirmView(RetrieveAPIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = 'completed'
        order.save()
        return Response({'message': 'Вы подтвердили заказ'}, status=200)