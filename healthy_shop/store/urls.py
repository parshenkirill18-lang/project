from django.urls import path
from .views import product_list

urlpatterns = [
    path('', product_list, name='product_list'),
]
from django.urls import path
from .views import product_list, register, user_login, user_logout

urlpatterns = [
    path('', product_list, name='product_list'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
from .views import add_to_cart, cart_detail

urlpatterns += [
    path('cart/', cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]
from .views import add_to_cart, cart_detail

urlpatterns += [
    path('cart/', cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]
from .views import increase_item, decrease_item, remove_item

urlpatterns += [
    path('cart/increase/<int:item_id>/', increase_item, name='increase_item'),
    path('cart/decrease/<int:item_id>/', decrease_item, name='decrease_item'),
    path('cart/remove/<int:item_id>/', remove_item, name='remove_item'),
]
from .views import checkout

urlpatterns += [
    path('checkout/', checkout, name='checkout'),
]
from .views import product_detail

urlpatterns += [
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
