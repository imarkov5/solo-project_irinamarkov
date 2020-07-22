from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from log_and_reg.models import *
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def one_collection(request, category):
    context = {
        'category': category,
        'all_products': Product.objects.all() 
    }
    print(category)
    return render(request, 'one_collection.html', context)

def cart(request):
    context = {
        'all_items': OrderItem.objects.all()
    }
    return render(request, 'cart.html', context)

def change_qty(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.quantity = int(request.POST['new_qty'])
    if item.quantity == 0:
        item.delete()
    else:
        item.save()
    
    return redirect('/cart')

def add_to_cart(request, product_id, category):
    OrderItem.objects.create(quantity=1, product=Product.objects.get(id=product_id))
    return redirect(f'/collections/{category}')

def checkout(request):
    if 'user_id' in request.session:
        all_items = OrderItem.objects.all()
        total_charge = 0
        order = Order.objects.create(user=User.objects.get(id=request.session['user_id']))
        for item in all_items:
            if order.user.id == request.session['user_id']:
                item.order = order
                item.save()
                total_price = item.product.price * item.quantity
                total_charge += total_price
        order.order_total = total_charge
        order.save()
        context = {
            'total_charge': total_charge,
            'all_items': all_items
        }
        
        return render(request, 'checkout.html', context)
    return redirect('/cart')

def admin_dashboard(request):
    if request.session['user_level'] == 9:
        context = {
            'all_orders': Order.objects.all()
        }
        return render(request, 'admin_dashboard.html', context)
    else:
        return redirect('/')

def show_order(request, order_id):
    if request.session['user_level'] == 9:
        order = Order.objects.get(id=order_id)
        all_items = order.item.all()
        context = {
            'order': Order.objects.get(id=order_id),
            'items_in_order': all_items
        }
    return render(request, 'one_order.html', context)

def products(request):
    if request.session['user_level'] == 9:
        context = {
            'all_products': Product.objects.all()
        }
        return render(request, 'all_products.html', context)
    else:
        return redirect('/')

def edit_product(request, product_id):
    if request.session['user_level'] == 9:
        context = {
            "product": Product.objects.get(id=product_id)
        }
        if request.method == "POST":
            product = Product.objects.get(id=product_id)
            product.category = request.POST['category']
            product.name = request.POST['name']
            product.description = request.POST['description']
            product.price = request.POST['price']
            product.quantity = request.POST['quantity']
            product.save()
            return redirect('/admin/products')
        return render(request, 'edit_product.html', context)
    return redirect('/')

def delete_product(request, product_id):
    Product.objects.get(id=product_id).delete()
    return redirect('/admin/products')

def add_new_product(request):
    if request.session['user_level'] == 9:
        if request.method == "POST":
            Product.objects.create(category=request.POST['category'], name=request.POST['name'], description=request.POST['description'], price=request.POST['price'], quantity=request.POST['quantity'], image=request.FILES['image'])
            return redirect('/admin/products')
        return render(request, 'add_new_product.html')
    return redirect('/')

def upload(request):
    pic = request.FILES['image']
    fs = FileSystemStorage()
    fs.save(pic.name, pic)
    return redirect('/admin/products/add_new_product')
    
