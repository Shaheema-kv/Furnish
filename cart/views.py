from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from store.models import Variation
from django.contrib.auth.decorators import login_required
from order.models import Address

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated:
        product_variation=[]
        if request.method == 'POST':
        
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation =Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass

    
        
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user ).exists()
        if is_cart_item_exists:
    
            cart_item = CartItem.objects.filter(product=product,  user=current_user)
           
            ex_var_list = []
            id =  []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            

            if product_variation in ex_var_list:
                # increase the cat item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
            
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
            
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
        
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product  = product,
                quantity = 1,
                user    = current_user,
            )
        
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
        
        

            cart_item.save()
        return redirect('cart')
    
    else:
        product_variation=[]
        if request.method == 'POST':
        
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation =Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass

    
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart ).exists()
        if is_cart_item_exists:
    
            cart_item = CartItem.objects.filter(product=product,  cart=cart)
            # existing variations -> database(come from)
            # current variation -> product_variation
            # cart_item_id ->database
            ex_var_list = []
            id =  []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cat item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
            
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
            
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
        
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product  = product,
                quantity = 1,
                cart     = cart,
            )
        
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
        
        

            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):#quantity decrement
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
                    cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
           cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):#remove button
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = tax + total
    except ObjectDoesNotExist:
        pass

    context={
        'total'   : total,
        'quantity': quantity,
        'cart_items':cart_items,
        'tax'     :  tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html',context)

@login_required(login_url='signin')
def checkout(request,   total=0, quantity=0, cart_items=None):
    print("checkout")
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = tax + total
    except ObjectDoesNotExist:
        pass
           
   
    
    address=Address.objects.filter(user=request.user)
    first_name=""
    last_name=""
    address1=""
    city=""
    state=""
    postalcode=""
    country = ""
    phone=""
    email=""
    usr=""
    if request.method == 'POST' :
            value= request.POST['adress']
            value=value.split('-')
            print(value)

            first_name=value[0]
            last_name=value[1]
            address1=value[2]
            city=value[3]
            state = value[4]
            postalcode=value[5]
            country = value[6]
            email=value[7]
            phone = value[8]
            usr=request.user

        
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'address' :address,
        'first_name' : first_name,
        'last_name' : last_name,
        'address1': address1,
        'city' : city,
        'state' : state,
        'postalcode' : postalcode,
        'country' : country,
        'email': email,
        'phone' : phone,
        'usr' :usr

        }
    return render(request, 'store/checkout.html',context)

def wishlist(request, wishitems=None):
    try:
        if request.user.is_authenticated:
            wishitems = Wishlist.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            wishitems = Wishlist.objects.filter(cart=cart, is_active = True)
    except ObjectDoesNotExist:
        pass
   
    context={
        'wishitems':wishitems,
    }
    return render(request, 'store/wishlist.html',context)


def add_to_wishlist(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    if current_user.is_authenticated:
        is_wishitem_exists = Wishlist.objects.filter(product=product, user=current_user ).exists()
        if is_wishitem_exists:
            pass
           
            
                
            

        else:
            wishitem = Wishlist.objects.create(
                product  = product,
                is_active = True,
                user    = current_user,
            )
            wishitem.save()
        return redirect('wishlist')
            
        
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_wishitem_exists = Wishlist.objects.filter(product=product, cart=cart ).exists()
        if is_wishitem_exists:
            pass
        else:
            
            wishitem = Wishlist.objects.create(
                product  = product,
                is_active =True,
                cart     = cart,
            )
            wishitem.save()
        return redirect('wishlist')
    
          
    

def remove_from_wishlist(request, wishlist_id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, cart=cart)
    wishlist_item.delete()
    return redirect('wishlist')
