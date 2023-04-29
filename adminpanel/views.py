from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from category.models import Categorie
from store.models import Product,Variation
from django.shortcuts import render,redirect
from .forms import ProductForm, CategoryForm, VariationForm
from order.models import Order, OrderProduct
from django.db.models import Q
from accounts.models import UserProfile

# Create your views here.

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def dashboard(request):
    cat   = Categorie.objects.all().count()
    prod  = Product.objects.filter(is_available=True).count()
    users = User.objects.all().count()
    context={
        'cat':cat,
        'prod':prod,
        'users':users
    }
    return render(request, 'adminpanel/dashboard.html',context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def user_management(request):
    users = User.objects.filter(is_superuser=False).order_by('id')
    userprofile = UserProfile()
    context={
        'users'       : users,
        'userprofile' : userprofile
        
    }
    return render(request, 'adminpanel/dashboard-users.html',context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def category_management(request):
    ctgry = Categorie.objects.all().order_by('id')
    context={
        'ctgry': ctgry
    }
    return render(request, 'adminpanel/dashboard-category.html',context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def product_management(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    context={
        'products': products
    }
    return render(request, 'adminpanel/dashboard-products.html',context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'adminpanel/dashboard-add-product.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        try:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
               
                return redirect('product_management')
            

        except Exception as e:
            raise e

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'adminpanel/dashboard-edit-product.html', context)


@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_management')
    else:
        form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, 'adminpanel/dashboard-add-category.html', context)
    

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def update_category(request, category_id):
    category = Categorie.objects.get(id=category_id)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        try:
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
               
                return redirect('product_management')
            

        except Exception as e:
            raise e

    context = {
        'category': category,
        'form': form
    }
    return render(request, 'adminpanel/dashboard-update-category.html', context)




@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_category(request, category_id):
    categories = Categorie.objects.get(id=category_id)
    categories.delete()

    return redirect('category_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def variation_management(request):
    variations = Variation.objects.all().order_by('id')

    context = {
        'variations': variations
    }
    return render(request, 'adminpanel/dashboard-variations.html',context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm()

    context = {
        'form': form
    }
    return render(request, 'adminpanel/dashboard-add-variation.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def update_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)

    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm(instance=variation)

    context = {
        'variation': variation,
        'form': form
    }
    return render(request, 'adminpanel/dashboard-update-variation.html',context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    variation.delete()
    return redirect('variation_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def order_management(request):
    orders = Order.objects.filter(is_ordered=True).order_by('id')
    ordered_products = OrderProduct.objects.filter(ordered=True)
    context={
        'orders' : orders,
        'ordered_products' : ordered_products,
    }
    return render(request, 'adminpanel/dashboard-order-management.html',context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def accept_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Shipped'
    order.save()

    return redirect('order_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def complete_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Delivered'
    order.save()

    return redirect('order_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def manager_cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('order_management')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('admin_order')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_order(request):
    current_user = request.user
    try:

        # if request.method == 'POST':
        #     keyword = request.POST['keyword']
        #     orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__contains=keyword) | Q(user__email__icontains=keyword) | Q(first_name__startswith=keyword) | Q(last_name__startswith=keyword) | Q(phone__startswith=keyword)).order_by('-created_at')

        # else:
        orders = Order.objects.filter(
            user=current_user, is_ordered=True).order_by('-created_at')
    except Exception as e:
        raise e
    
    context = {
        'orders': orders,
    }
    return render(request, 'adminpanel/dashboard-admin_order.html', context)

    

