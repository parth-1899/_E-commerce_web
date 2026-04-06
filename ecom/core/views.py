from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #  VERY IMPORTANT
            user.set_password(form.cleaned_data['password'])

            user.save()

            user.profile.role = form.cleaned_data['role']
            user.profile.save()

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Admin check
            if user.is_superuser:
                return redirect('/admin/')

            # ✅ Safe profile access
            if hasattr(user, 'profile'):
                role = user.profile.role.lower()

                print("ROLE:", role)  # debug

                if role == 'seller':
                    return redirect('add_product')

            # ✅ Default (buyer)
            return redirect('product_list')

        else:
            print("LOGIN FAILED")

    return render(request, 'login.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')

def test(request):
    return render(request, 'login.html')

from .forms import SellerForm
from .models import SellerProfile

def seller_register(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            return redirect('home')
    
    else:
        form = SellerForm()
    
    return render(request, 'seller_register.html', {'form': form})

def add_product(request):
    if not request.user.sellerprofile.is_verified:
        return HttpResponse("You are not verified!")
    
    # allow adding product

from .forms import ProductForm
from django.http import HttpResponse

def add_product(request):

    #  Allow only verified sellers
    if not hasattr(request.user, 'sellerprofile') or not request.user.sellerprofile.is_verified:
        return HttpResponse("You are not verified!")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


from .models import Order, Product

def buy_product(request, product_id):
    product = Product.objects.get(id=product_id)

    Order.objects.create(
        user=request.user,
        product=product,
        quantity=1
    )

    return HttpResponse("Order Placed Successfully!")

# for hiome url
def home(request):
    return render(request, 'home.html')