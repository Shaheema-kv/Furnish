
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('profile/',views.profile,name='profile'),
    path('signout/',views.signout,name='signout'),
    path('account_profile/',views.account_profile,name='account_profile'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('my_addresses/',views.my_addresses,name='my_addresses'),
    path('add_address/',views.add_address,name='add_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('delete_address/<int:address_id>/',views.delete_address,name='delete_address'),
    # path('orders/', views.orders, name='orders'),
    path('cancel_order_user/<int:order_number>', views.cancel_order_user, name="cancel_order_user"),
    


]