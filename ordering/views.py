from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from ordering.models import Food, Testimonial, Catering, Profile, Order, OrderItems
from collections import Counter
from django.contrib import messages
from ordering.forms import ContactForm, RegisterForm, LoginForm
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from ordering.forms import ProfileForm
import requests
from requests.auth import HTTPBasicAuth



def paymongo_gcash(amount):
    final_amount = str(amount) + '00'
    url = "https://api.paymongo.com/v1/sources"

    payload = {"data": {"attributes": {
                "amount": int(final_amount),
                "redirect": {
                    "success": "http://127.0.0.1:8000",
                    "failed": "http://127.0.0.1:8001"
                },
                "billing": {
                    "name": "test",
                    "phone": "09631230987",
                    "email": "example@email.com"
                },
                "type": "gcash",
                "currency": "PHP"
            }}}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        
    }

    response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth('pk_test_VCsn3f8Rv4kvBNeVRjQZezK4', 'sk_test_eX67HqRLhcsmeh6TtUBAbaoM'))

    data = response.json()

    return data['data']['attributes']['redirect']['checkout_url']



def my_send_mail(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        send_mail(
            f"Message from {name}.",
            f"{message}",
            f"{email}",
            ['example@email.com'],
            fail_silently=True,
        )
        form = ContactForm()
        messages.success(request, "Success.. Email Sent")
        return form
    
    messages.error(request, "Error.. Something Wrong")
    return form


class IndexView(View):

    def get(self, request):
        form = ContactForm()
        testimonials = Testimonial.objects.all()[:3]
        bests = Food.objects.filter(status="Best Seller")[:1]
        foods = Food.objects.exclude(
            Q(status="Best Seller") | Q(status="Out Of Stock"))
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        context = {
            'testimonials': testimonials,
            'foods': foods,
            'bests': bests,
            'cart': len(cart),
            'form': form
        }

        return render(request, 'index.html', context)
    
    def post(self, request):
        form = my_send_mail(request)
        testimonials = Testimonial.objects.all()[:3]
        bests = Food.objects.filter(status="Best Seller")[:1]
        foods = Food.objects.exclude(
            Q(status="Best Seller") | Q(status="Out Of Stock"))
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        context = {
            'testimonials': testimonials,
            'foods': foods,
            'bests': bests,
            'cart': len(cart),
            'form': form
        }
        return render(request, 'index.html', context)


class AboutView(View):

    def get(self, request):
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        context = {
            'cart': len(cart)
        }
        return render(request, 'about.html', context)


class ServiceView(View):

    def get(self, request):
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        catering = Catering.objects.all()
        context = {
            'cart': len(cart),
            'catering': catering
        }

        return render(request, 'service.html', context)


class ContactView(View):

    def get(self, request):
        form = ContactForm()
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        context = {
            'cart': len(cart),
            'form': form
        }

        return render(request, 'contact.html', context)

    def post(self, request):
        form = my_send_mail(request)
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)


class AddtocartView(View):

    def get(self, request, pk):

        if 'cart' in self.request.session:
            self.request.session['cart'].append(pk)

        else:
            self.request.session['cart'] = [pk]

        self.request.session.modified = True
        cart = self.request.session['cart']

        messages.success(request, 'Success.. Added successfully')

        return render(request, 'htmx_partials/add_to_cart_partial.html', {'cart': len(cart)})


class CartView(View):

    def get_total(self, list_items):
        if isinstance(list_items, list):
            total = 0
            for item in list_items:
                food = Food.objects.get(pk=item)
                total += food.price

            return total

        else:
            return "not a list"

    def get(self, request):
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        foods = Food.objects.filter(pk__in=cart)
        c = Counter(cart)
        total = self.get_total(cart)
        context = {
            'cart': len(cart),
            'foods': foods,
            'counter': dict(c),
            'total': total
        }
        return render(request, 'cart.html', context)


class DeleteItemInCartView(View):

    def post(self, request, pk):
        count = len(self.request.session['cart'])
        for i in range(count):
            if pk in self.request.session['cart']:
                self.request.session['cart'].remove(pk)

        self.request.session.modified = True

        return redirect(reverse('cart'))


class UpdateQntyInCartView(View):

    def post(self, request, pk):
        qnty = request.POST.get('qty')
        action = request.POST.get('action')

        if action == "+":
            if int(qnty) < 10:
                self.request.session['cart'].append(pk)
                request.session.modified = True
            else:
                messages.error(request, "Error.. Max quantity is 10")
        elif action == "-":
            if int(qnty) > 1:
                self.request.session['cart'].remove(pk)
                request.session.modified = True
            else:
                messages.error(request, "Error.. Minimum quantity is 1")
        return redirect(reverse('cart'))


class DetailView(DetailView):
    template_name = "detail_full_view.html"
    model = Food
    context_object_name = "food"


class CheckOut(View):


    def get(self, request):
        
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        

        if cart == []:
            messages.error(request, "Error.. Your cart is empty")
            return redirect('cart')

        if not request.user.is_authenticated:
            messages.error(request, "You're not logged in please log in")
            return redirect('cart')
        
        user = User.objects.get(pk=request.user.pk)
        profile = Profile.objects.get(user=user)
        cart_items = Food.objects.filter(pk__in=cart)
        c = Counter(cart)
        total = CartView().get_total(cart)
        shipping = 50
        final_total = total + shipping
        context = {
            'cart': len(cart),
            'profile': profile,
            'cart_items': cart_items,
            'counter': dict(c),
            'shipping': shipping,
            'final_total': final_total
        }

        return render(request, 'checkout.html', context)

   


class SigninView(View):

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        context = {
            'form': form,
            'cart': len(cart)
        }
        return render(request, 'signin.html', context)


    
    def get(self, request):
        form = LoginForm(request)
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        if request.user.is_authenticated:
            return redirect('/')
        context = {
            'form': form,
            'cart': len(cart)
        }

        return render(request, 'signin.html', context)



class SignupView(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        if form.is_valid():
            form.save()
            messages.success(request, "Success! Registered successfully")
            return redirect('/')
        
        context = {
            'form': form,
            'cart':len(cart)
        }
        return render(request, 'signup.html', context)

    def get(self, request):
        form = RegisterForm()
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []
        if request.user.is_authenticated:
            return redirect('/')

        context = {
            'form': form,
            'cart':len(cart)
        }
        return render(request, 'signup.html', context)


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/')

class ProfileView(LoginRequiredMixin ,View):
    login_url = '/login/'

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        profile = Profile.objects.get(user=user)
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        context = {
            'cart': len(cart),
            'profile': profile
        }

        return render(request, 'profile.html', context)

class ProfileEditView(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        instance = Profile.objects.get(user=user)
        form = ProfileForm(instance=instance)

        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        context = {
            'form': form,
            'cart': len(cart)
        }

        return render(request, 'profile_edit.html', context)

    def post(self,request):
        user = User.objects.get(pk=request.user.pk)
        instance = Profile.objects.get(user=user)
        form = ProfileForm(request.POST or None, instance=instance)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Success! Profile Updated")
            return redirect(reverse('profile'))

        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        context = {
            'form': form,
            'cart': len(cart)
        } 
        
        messages.error(request, "Error! Please try again")
        return render(request, 'profile_edit.html', context)

class OrderView(LoginRequiredMixin, View):

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        profile = Profile.objects.get(user=user)
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        if profile.first_name == None or profile.last_name == None or profile.address == None or profile.cellphone_number == None:
            messages.error(request, 'Error! Please provide your information')
            return redirect(reverse('checkout'))

        sub_total = CartView().get_total(cart)
        c = Counter(cart)
        dict_counter = dict(c)
        payment_method = request.POST['payment']
        shipping_fee = request.POST['shipping']
        total = int(sub_total) + int(shipping_fee)
        
        if payment_method == 'GCASH':
            paid_status = 'Paid'
            payment = 'Gcash'
        elif payment_method == 'COD':
            paid_status = 'Unpaid'
            payment = 'COD'

        order = Order.objects.create(
            user=user,
            total=total,
            shipping_fee=int(shipping_fee),
            payment_method=payment,
            paid_status=paid_status,
        )
        order.save()

        for key in dict_counter:
            food = Food.objects.get(pk=key)
            order_items = OrderItems.objects.create(
                order = order,
                food = food,
                quantity = int(dict_counter[key])
            )
        
        order_items.save()

        context = {

        }
            
        return render(request, 'order_detail.html', context)