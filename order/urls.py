from django.urls import path
from order.views import OrderAPIView, OrderConfirmView

urlpatterns = [
    path('',OrderAPIView.as_view()),
    path('confirm/<int:pk>/' ,OrderConfirmView.as_view())
]