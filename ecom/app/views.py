from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from product.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import *
from order.models import ShopCart

# Create your views here.
def index(request):
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    products = Product.objects.all().order_by('?')
    current_user = request.user  
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_qty=0
    total = 0
    for rs in shopcart:
        total += rs.amount
        total_qty += rs.quantity
    context = {
        'sliderdata': sliderdata,
        # 'page': 'home',
        'products': products,
        'category': category,
        'total_qty': total_qty,
        'total':total
    }
    return render(request, 'index.html', context)

def category_products(request, id, slug):
    current_user = request.user  
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_qty=0
    total = 0
    for rs in shopcart:
        total += rs.amount
        total_qty += rs.quantity
    context = {
        'products': products,
        'category': category,
        'categorydata': categorydata,
        'total_qty': total_qty,
        'total':total
    }
    return render(request, 'products.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Error! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
    }
    return render(request, 'signup.html', context)

def product_detail(request,id,slug):
    current_user = request.user  
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_qty=0
    total = 0
    for rs in shopcart:
        total += rs.amount
        total_qty += rs.quantity
    context = {
        'product': product,
        'category': category,
        'images': images,
        'total_qty': total_qty,
        'total':total
    }
    return render(request, 'product_details.html', context)
