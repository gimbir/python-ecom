from django.contrib.auth import login
from django.http.response import HttpResponse, HttpResponseRedirect
from product.models import *
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from order.models import ShopCart, ShopCartForm

# Create your views here.
def index(request):
    return HttpResponse('test')

@login_required(login_url='/login')
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user  

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data=ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Urun sepete eklendi')
        return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Urun sepete eklendi')
        return HttpResponseRedirect(url)
    
def cart(request):
    category = Category.objects.all()
    current_user = request.user  
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_qty=0
    total = 0
    for rs in shopcart:
        total += rs.amount
        total_qty += rs.quantity
    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             'total_qty':total_qty,
             }
    return render(request,'cart.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'Urun sepetten silindi')
    return HttpResponseRedirect('/cart')
