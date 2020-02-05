from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView,View
from product.models import Product,OrderProduct,Order, ShippingAddress,Payment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from product.forms import CheckOutForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist



import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



# Create your views here.

class HomeView(ListView):
    model=Product
    paginate_by=6
    template_name="product/index.html"

def search_func(request):
    search_word=request.GET.get('name_or_category')
    if search_word != "" and search_word is not None:
        qs=Product.objects.filter(Q(name__icontains=search_word)|Q(category__icontains=search_word))
        context={
            'results':qs
        }

        return render(request, 'product/search.html',context)
    
class CheckOutView(View):
    def get(self, *args, **kwargs):
        form=CheckOutForm()
        order=Order.objects.get(user=self.request.user, ordered=False)
        context={
            'form':form,
             'order':order
        }
        return render(self.request, "product/checkout.html",context)
    def post(self, *args, **kwargs):
        form=CheckOutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                building_no=form.cleaned_data.get('building_number')
                street_name=form.cleaned_data.get('street_name')
                area=form.cleaned_data.get('area')
                city=form.cleaned_data.get('city')
                #todo later 
               # save_as_default=form.cleaned_data.get('save_as_default')
                payment_option=form.cleaned_data.get('payment_option')

                shipping_address=ShippingAddress(
                    user=self.request.user,
                    apartment_no=building_no,
                    street_name=street_name,
                    area=area,
                    city=city
                )
                shipping_address.save()
                order.shipping_address=shipping_address
                order.save()

                if payment_option == 'C':
                    return redirect('payment', payment_option='credit-card')
                elif payment_option =='P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "invalid payment option")
                    return redirect('checkout')
                
            messages.warning(self.request, "failed checkout")
            return redirect("checkout")
           
        except ObjectDoesNotExist:
            messages.warning(self.request, "you do not have an active order")
            return redirect( "order_summary")







class PaymentView(View):
    def get(self, *args, **kwargs):
        order=Order.objects.get(user=self.request.user, ordered=False)
        if order.shipping_address:
            context={
                'order':order
            }
            return render(self.request, "product/payment.html", context)
        else:
            messages.warning(self.request, "you have not filling the shipping address")
            return redirect('checkout')
    def post(self, *args, **kwargs):
        order=Order.objects.get(user=self.request.user, ordered=False)
        token=self.request.POST.get('stripeToken') 
        amount=int(order.get_total()*100)
        print(amount)
        print(token)
        try:
            charge=stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                )
            payment=Payment()
            payment.stripe_charge_id=charge['id']
            payment.user=self.request.user
            payment.amount=order.get_total()

            payment.save()

            order_items= order.products.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered=True
            order.payment=payment
            order.ref_code=create_ref_code()
            order.save()
            messages.success(self.request, "your order was successful")
            return redirect('profile')
        except stripe.error.CardError as e:
            messages.warning(self.request, f"{e.error.message}")
            return redirect("/") 
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "invalid parameter")
            return redirect("payment", payment_option='credit-card')
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.warning(self.request, "authentication error occurred")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error occurred")
            return redirect("/")
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.warning(self.request, "something went wrong, please try again later")
            return redirect("/")
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            messages.warning(self.request,"a serious error occurred, an email has be sent to the admin")
            return redirect("/")

         
        

class ProductDetailView(DetailView):
    model=Product
    template_name="product/detail.html"

class Order_Summary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':order
            }
            return render(self.request, "product/order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "you do not have an active order")

            return redirect( "home")
    
@login_required
def add_to_cart(request, slug):
    item =get_object_or_404(Product, slug=slug)
    order_product, created =OrderProduct.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]

        if order.products.filter(item__slug=item.slug).exists():
            order_product.quantity +=1
            order_product.save()
            messages.info(request, "item quantity  increased") 
            return redirect("order_summary")
        else:
            messages.info(request, "this item was added to your cart")
            order.products.add(order_product)
            return redirect("order_summary")         
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(
                    user=request.user,
                    ordered_date=ordered_date
                    )
        messages.info(request,"this item was added to your cart")
        order.products.add(order_product)
    return redirect("product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item =get_object_or_404(Product, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]

        if order.products.filter(item__slug=item.slug).exists():
            order_product=OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product) 
            messages.success(request, "this item was remove from your cart")
            return redirect("order_summary")
        else:
            messages.warning(request,"you do not have this item in your  cart")
            return redirect("product", slug=slug)
        

    else:
        messages.warning(request,"you do not have an active order")
        return redirect("product", slug=slug)

    return redirect("product",slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    item =get_object_or_404(Product, slug=slug)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]

        if order.products.filter(item__slug=item.slug).exists():
            order_product=OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity >1:
                 order_product.quantity -=1
                 order_product.save()
            else:
                order.products.remove(order_product)
            messages.success(request, " item quantity was decreased")
            return redirect("order_summary")
        else:
            messages.warning(request,"you do not have this item in your  cart")
            return redirect("order_summary")
        

    else:
        messages.warning(request,"you do not have an active order")
        return redirect("product", slug=slug)

    return redirect("product",slug=slug)


class Menu_View(View):
    def get(self, *args, **kwargs):
        products=Product.objects.all()
        context={
            'items':products
        }
        return render(self.request, "product/menu.html", context) 


class Contact_View(View):
    def get(self, *args, **kwargs):
        return render(self.request, "product/contact.html" )