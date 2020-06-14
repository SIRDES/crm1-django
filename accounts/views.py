from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .form import *
from .filter import *
from .decorators import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
@allowed_user(allow_rolls=['admin'])
def dashboard(request):
    customers = Customer.objects.all()
    orders= Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    context = {'customers':customers, 'orders':orders,'pending':pending,'delivered':delivered,'total_customers':total_customers,'total_orders':total_orders}

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()
    
    myFilter = orderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customers':customers, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}

    return render(request, 'customers.html', context)

def createOrder(request):
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
       
    context = {'form':form}
    return render(request, 'create_order.html', context)

def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'customerform.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'create_order.html', context)

def deleteOrder(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item':item}
    return render(request, 'deleteOrder.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect ('login')

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)

    return render(request, 'index.html')


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name= 'customer')
            user.groups.add(group)

            Customer.objects.Create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
@allowed_user(allow_rolls=['customer'])
def userProfile(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()

    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()

    context = {'orders':orders, 'total_orders':total_orders,'pending':pending,'delivered':delivered}
    return render(request, 'userProfile.html', context)

@login_required(login_url='login')
@allowed_user(allow_rolls=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method =='POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'account_settings.html', context)