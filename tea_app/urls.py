from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('collections/<str:category>', views.one_collection),
    path('cart', views.cart),
    path('cart/change_qty/<int:item_id>', views.change_qty),
    path('add_to_cart/<int:product_id>/<str:category>', views.add_to_cart),
    path('checkout', views.checkout),
    path('admin/dashboard', views.admin_dashboard),
    path('admin/show_order/<int:order_id>', views.show_order),
    path('admin/products', views.products),
    path('admin/products/edit/<int:product_id>', views.edit_product),
    path('admin/products/delete/<int:product_id>', views.delete_product),
    path('admin/products/add_new_product', views.add_new_product),
    path('upload', views.upload),
]