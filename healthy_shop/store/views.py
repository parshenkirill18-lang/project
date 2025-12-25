from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, 'store/products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('product_list')
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})
from django.views.decorators.http import require_POST

@require_POST
@login_required
def increase_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_detail')

@require_POST
@login_required
def decrease_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_detail')

@require_POST
@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_detail')
from .forms import OrderForm
from django.contrib import messages

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('product_list')

    total = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.save()
            items.delete()  # очищаем корзину после заказа
            messages.success(request, "Заказ успешно оформлен!")
            return redirect('product_list')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {'form': form, 'total': total})
from django.shortcuts import get_object_or_404

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})
