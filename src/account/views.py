from django.shortcuts import render,redirect
from account.forms import RegisterationForm, AccountAuthenticationForm,UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from product.models import Order
# Create your views here.

def registeration_view(request):
    context={ }
    if request.POST:
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password=form.cleaned_data.get('password1')
            account =authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('profile')

        else:
            context['register_form']=form
    
    else:
        form=RegisterationForm()
        context['register_form']=form

    return render(request, 'account/register.html', context)


def login_view(request):
    context={}
    user= request.user
    if user.is_authenticated:
        return redirect('profile')

    if request.POST:
        form =AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email= request.POST['email']
            password = request.POST['password']
            user= authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('profile')
    else:
        form=AccountAuthenticationForm()

    context['login_form']=form
    return render(request, 'account/login.html', context)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.POST:
        form=UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form=UserProfileUpdateForm(
            initial={
                "email":request.user.email,
                "username":request.user.username,
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,
                "phone":request.user.phone
            }
        )
        order=Order.objects.filter(user=request.user, ordered=True)
    context={
        'user':request.user,
        'orders':order,
        "account_form":form
    }
    return render(request, 'account/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def track_order(request):
    order=Order.objects.filter(user=request.user, ordered=True)
    track_code=request.POST.get('track_order')
    if track_code != '' and track_code is not None:
        track_qs=order.get(ref_code__iexact=track_code)
    context={
        'msgs':track_qs
    }
    return render(request, 'account/profile.html',context)
