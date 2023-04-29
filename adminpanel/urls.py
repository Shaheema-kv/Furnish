
from django.urls import path
from .import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('users/',views.user_management,name='user_management'),
    path('categories/',views.category_management,name='category_management'),
    path('products/',views.product_management,name='product_management'),
    path('block_user/<int:user_id>/',views.block_user,name="block_user"),
    path('unblock_user/<int:user_id>/',views.unblock_user,name='unblock_user'),
    path('add_new_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('add_category/', views.add_category, name="add_category"),
    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    path('variation_management/',views.variation_management,name='variation_management'),
    path('add_variation/', views.add_variation, name="add_variation"),
    path('update_variation/<int:variation_id>/', views.update_variation, name="update_variation"),
    path('delete_variation/<int:variation_id>/',views.delete_variation,name='delete_variation'),
    path('order_management/',views.order_management,name='order_management'),
    path('admin_orders/', views.admin_order, name="admin_orders"),
    path('accept_order/<int:order_number>/', views.accept_order, name='accept_order'),
    path('complete_order/<int:order_number>/', views.complete_order, name='complete_order'),
    path('manager_cancel_order/<int:order_number>/', views.manager_cancel_order, name='manager_cancel_order'),
    path('cancel_order/<int:order_number>/', views.cancel_order, name='cancel_order'),
]