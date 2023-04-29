from django.http import JsonResponse
from django.shortcuts import render, redirect
from cart.models import CartItem , Cart
from .forms import OrderForm
from store.models import Product
from .models import Order, OrderProduct, Payment
import datetime
from django.contrib.auth.decorators import login_required
from order.models import Address
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
# Create your views here.


def payments(request):
    print("payment")
    cartitem = CartItem.objects.filter(user=request.user)
    if cartitem == None:
        return redirect('home')
    else:
        return render(request, 'orders/payments.html')

@never_cache
def place_order(request, total=0, quantity=0):
    print("place_order")
    cartitem = CartItem.objects.filter(user=request.user)
    if cartitem == None:
        print("payment - home")
        return HttpResponseRedirect(reverse('home'))
        # return redirect('home')
    else:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('store')
        
        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                
                    pt=form.cleaned_data['address_1']
                    nm=form.cleaned_data['first_name']
                    # ln=form.cleaned_data['last_name']
                    print(pt,'this address')
                    if Address.objects.filter(user=request.user,first_name=nm,address=pt) :
                        check = True

                    else :
                        check=False
                        
                    
                    print(check)
                    add=Address()
                    if check == False :
                        add.user=request.user
                        add.first_name = form.cleaned_data['first_name']
                        add.last_name = form.cleaned_data['last_name']
                        add.address = form.cleaned_data['address_1']
                        add.city = form.cleaned_data['city']
                        add.state=form.cleaned_data['state']
                        add.country=form.cleaned_data['country']
                        add.email=form.cleaned_data['email']
                        add.phone= form.cleaned_data['phone']
                        add.save()

                        data = Order()
                        data.user = current_user
                        data.first_name = form.cleaned_data['first_name']
                        data.last_name = form.cleaned_data['last_name']
                        data.phone = form.cleaned_data['phone']
                        data.email = form.cleaned_data['email']
                        data.address_1 = form.cleaned_data['address_1']
                        data.address_2 = form.cleaned_data['address_2']
                        data.country = form.cleaned_data['country']
                        data.state = form.cleaned_data['state']
                        data.city = form.cleaned_data['city']
                        data.order_note = form.cleaned_data['order_note'] 
                        data.order_total = grand_total
                        data.tax = tax
                        data.ip = request.META.get('REMOTE_ADDR')
                        data.save()   
    #             # generate order number
                        yr = int(datetime.date.today().strftime('%Y'))
                        dt = int(datetime.date.today().strftime('%d'))
                        mt = int(datetime.date.today().strftime('%m'))
                        d  = datetime.date(yr,mt,dt)
                        current_date = d.strftime("%Y%m%d")
                        order_number = current_date + str(data.id)
                        data.order_number = order_number
                        data.save()
                        data_product = OrderProduct()

                        
                        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                        context = {
                            'order': order,
                            'cart_items': cart_items,
                            'total': total,
                            'tax': tax,
                            'grand_total': grand_total,
                        }
                        return render(request, 'orders/payments.html', context)
                
                    else:
                        data = Order()
                        data.user = current_user
                        data.first_name = form.cleaned_data['first_name']
                        data.last_name = form.cleaned_data['last_name']
                        data.phone = form.cleaned_data['phone']
                        data.email = form.cleaned_data['email']
                        data.address_1 = form.cleaned_data['address_1']
                        data.address_2 = form.cleaned_data['address_2']
                        data.country = form.cleaned_data['country']
                        data.state = form.cleaned_data['state']
                        data.city = form.cleaned_data['city']
                        data.order_note = form.cleaned_data['order_note']
                        data.order_total = grand_total
                        data.tax = tax
                        data.ip = request.META.get('REMOTE_ADDR')
                        data.save()
                        # Generate order number
                        yr = int(datetime.date.today().strftime('%Y'))
                        dt = int(datetime.date.today().strftime('%d'))
                        mt = int(datetime.date.today().strftime('%m'))
                        d = datetime.date(yr,mt,dt)
                        current_date = d.strftime("%Y%m%d") #20210305
                        order_number = current_date + str(data.id)
                        data.order_number = order_number
                        data.save()
                        data_product = OrderProduct()
                        
                        

                        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                        context = {
                            'order': order,
                            'cart_items': cart_items,
                            'total': total,
                            'tax': tax,
                            'grand_total': grand_total,
                        }
                        return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
    


# @cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='login')
def razorpaycheck(request):
    print('this arazorpay check ')
    if request.method == "POST":
        payment_order = Payment()
        payment_order.user = request.user
        payment_order.payment_method = request.POST.get('payment_mode')
        if request.POST.get('payment_id'):
            payment_order.payment_id = request.POST.get('payment_id')
        payment_order.amount_paid = request.POST.get('grand_total')
        payment_order.status = True
        # payment_order.status=request.POST.get('status')
        payment_order.save()
        print("payment is saved")

        order_number = request.POST.get('order_no')
        order = Order.objects.get(user=request.user, order_number=order_number)
        order.Payment = payment_order
        order.is_ordered = True
        order.status = 'Processing'
        print('order status updated============================')
        print("Grand total", request.POST.get('grand_total'))
        order.order_total = request.POST.get('grand_total')
        print(order.order_total)

        print('order total are updated ============================')
        order.save()
         

        # moving the order details into order product table

        cart_items = CartItem.objects.filter(user=request.user)
        print(cart_items,"hi")
        
        for cart_item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment_order
            order_product.user = request.user
            order_product.product = cart_item.product
            order_product.quantity = cart_item.quantity
            order_product.product_price = cart_item.product.price
            order_product.ordered = True
            order_product.save()
            item = CartItem.objects.get(id=cart_item.id)
            product_variation = item.variations.all()
            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variation.set(product_variation)
            order_product.save()

            # reducing the quantity of product after selling it
            product = Product.objects.get(id=cart_item.product_id)
            product.stock -= cart_item.quantity
            product.save()

        # deleting the cart items
        CartItem.objects.filter(user=request.user).delete()

        # send order number and transaction id

        data = {
            'order_number': order_number,
            'tansID': payment_order.payment_id,
        }
        print("completed")
        # return render(request,'orders/order_completed.html')
        return JsonResponse({'status': 'Your order placed successfully!','data':data})
    
# @cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='login')
def order_completed(request):
    order_number = request.GET.get('order_number')
    print(order_number)

    # # Add the following code to prevent going back to previous pages
    # response = HttpResponseRedirect(reverse('cart'))
    # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'        
    # response['Pragma'] = 'no-cache'
    # response['Expires'] = '0'

    try:
        order = Order.objects.get(order_number=order_number)
        order.status = 'Accepted'
        order.save()
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = order.order_total-order.tax



        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'sub_total': subtotal
        }
        return render(request, 'orders/order_complete.html', context)

        

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
        
        
# @login_required(login_url='login')
# def delete_address(request, address_id):
#     address = Address.objects.get(id=address_id)
#     address.delete()
#     return redirect('checkout')

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_detail.html', context)

