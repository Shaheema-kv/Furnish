from django.urls import path
from .import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name="payments"),
    path('proceed-to-pay/',views.razorpaycheck, name="razorpaycheck"),
    path('order-completed/', views.order_completed, name="order_completed"),
    path('order_detail/<int:order_id>/',views.order_detail, name="order_detail"),


]