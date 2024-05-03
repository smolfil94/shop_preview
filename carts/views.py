from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import CartItem
from .forms import CartAddProductForm

from products.models import Product


@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'cart.html', {'cart_items': cart_items})


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('cart')


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        cart_item.delete()
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class UpdateCartItemView(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item.quantity = quantity
            cart_item.save()
        return redirect('cart')
