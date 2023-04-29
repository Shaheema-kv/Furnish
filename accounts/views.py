from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from .models import UserOTP, UserProfile
from django.core.mail import send_mail
from .models import UserOTP
from django.conf import settings
from category.models import Categorie
from store.models import Product
from cart.models import Cart, CartItem, Wishlist
from order.models import Order,Address
from .forms import UserProfileForm, UserForm, AddressForm
from cart.views import _cart_id

# Create your views here.
def home (request):
    ctgry = Categorie.objects.all()
    product = Product.objects.filter(is_available=True)
    return render(request, 'index.html',{'ctgry': ctgry, 'product':product})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            # get_otp = request.POST.get('otp')
            get_otp = request.POST.get('otp')
            if get_otp:
                get_usr = request.POST.get('usr')
                usr = User.objects.get(username=get_usr)
                # if not usr.is_active:
                if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active= True
                    usr.save()
                    messages.success(request, f'Account is Created for {usr.username}')
                    return redirect('signin')
                else:
                    messages.error(request, f'You  entered a wrong OTP')
                    return render(request, 'signup.html',{'otp':True,'usr':usr})

            

            
            urnm = request.POST['username']                                                     
            ftnm = request.POST['firstname']
            ltnm = request.POST['lastname']
            pw   = request.POST['password1'] 
            pw2  = request.POST['password2']   
                                                                                    
            if pw == pw2:
                if User.objects.filter(username=urnm).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('signup')
                    
                else:
                    registration = User.objects.create_user(username=urnm, first_name=ftnm,  last_name=ltnm, password=pw, is_active=False)
                        
                    registration.save()
                            # messages.info(request, 'Succefully Created your Account')
                            # send_mail('Subject here', 'Here is the message.', 'skvshaheema@gmail.com', ['skvshaheema@gmail.com'], fail_silently=False)
                    usr = User.objects.get(username=urnm)
                    usr_otp = random.randint(100000, 999999)
                    UserOTP.objects.create(user = usr, otp = usr_otp)
                    mess = f"Hello ,\nYour OTP is {usr_otp}\nThanks!"

                    send_mail(
                        "Welome to Furnish - verify your email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.username],
                        fail_silently = False

                    )
                    return render(request, 'signup.html',{'otp':True,'usr':usr})
                        # return render(request, 'otp.html')
            else:
                messages.info(request, 'Password not match')
                return render(request, 'signup.html')        
    return render(request, 'signup.html')
             
                
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)


            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_wishitem_exists = Wishlist.objects.filter(cart=cart).exists()
                            
                    if is_wishitem_exists:
                        wishitem = Wishlist.objects.filter(cart=cart)
                        for item in wishitem:
                            item.user = user
                            item.save()
                except:
                    pass


            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter( cart=cart).exists()
                    
                

                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))
                        
                        cart_item = CartItem.objects.filter( user=user)
                        ex_var_list = []
                        id =  []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        
                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                        # for item in cart_item:
                        #     item.user = user
                        #     item.save()
                except:
                    pass
                login(request, user)
                return redirect('home')    
            
            else:
                messages.error(request, 'Incorrect Username or Password')
                return redirect('signin')
        
        return render(request, 'signin.html')

def profile(request):
    return render(request, 'account-profile.html')

@login_required(login_url='signin')
def signout(request):
        logout(request)
        messages.success(request, "Logout successfully")
        return redirect('signin')


@login_required(login_url='signin')
def account_profile(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
        
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        userprofile = None
    if request.method == 'POST':
        
        
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user  # Set the user field to the current user
            profile.save()
            messages.success(request, "Your profile has been updated")
            return redirect('account_profile')
    else:
        
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile, initial={'user': request.user})
    try:
        profile_picture_url = userprofile.profile_picture.url  # Get the URL to the saved image
    except:
        profile_picture_url = None

    context = {
        'orders_count': orders_count,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture_url': profile_picture_url,  # Pass the URL to the template
    }
    return render(request, 'user_profile/account-profile.html', context)

# @login_required(login_url='login')
# def my_orders(request):
#     orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
#     context = {
#         'orders': orders,
#     }
#     return render(request, 'user_profile/account-orders.html', context)

@login_required(login_url='signin')
def my_orders(request):
    orders = Order.objects.filter(user_id = request.user, is_ordered = True).order_by('-created_at')
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        userprofile = None
    try:
        profile_picture_url = userprofile.profile_picture.url  # Get the URL to the saved image
    except:
        profile_picture_url = None
    context={
        'orders':orders,
        'orders_count': orders_count,
        'profile_picture_url': profile_picture_url,
    }
    return render(request, 'user_profile/account-orders.html', context )



@login_required(login_url='signin')
def cancel_order_user(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order.status = 'Cancelled'
        order.save()

        return redirect('my_orders')
        
    except Exception as e:
        raise e


@login_required(login_url='signin')
def my_addresses(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        userprofile = None
    address = Address.objects.filter(user=request.user)
    try:
        profile_picture_url = userprofile.profile_picture.url  # Get the URL to the saved image
    except:
        profile_picture_url = None
    context={
        'profile_picture_url': profile_picture_url,
        'orders_count': orders_count,
        'address' : address,
    }
    return render(request, 'user_profile/account-address.html', context)

@login_required(login_url='signin')
def edit_address(request, address_id):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        userprofile = None
    try:
        profile_picture_url = userprofile.profile_picture.url  # Get the URL to the saved image
    except:
        profile_picture_url = None
    address = Address.objects.get(id=address_id)
    form = AddressForm(instance=address)
    if request.method == 'POST':
        try:
            form = AddressForm(request.POST,  instance=address)
            if form.is_valid():
                form.save()
               
                return redirect('my_addresses')
            

        except Exception as e:
            raise e
    
    context={
        'address' : address,
        'form'    : form,
        'profile_picture_url': profile_picture_url,
        'orders_count': orders_count,
    }
    return render(request, 'user_profile/edit_address.html',context)


@login_required(login_url='signin')
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    return redirect('my_addresses')

@login_required(login_url='signin')
def add_address(request):
    
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist gracefully
        userprofile = None
    try:
        profile_picture_url = userprofile.profile_picture.url  # Get the URL to the saved image
    except:
        profile_picture_url = None
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            return redirect('my_addresses')
    else:
        form = AddressForm()
        context = {
            'form': form,
            'profile_picture_url': profile_picture_url,
            'orders_count': orders_count,
        }
    return render(request, 'user_profile/add_address.html',context)






