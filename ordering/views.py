from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from ordering.models import Food, Testimonial, Catering, Checkout
from collections import Counter
from django.contrib import messages
from ordering.forms import CheckoutForm, ContactForm, RegisterForm, LoginForm
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import logout, login


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


        form = CheckoutForm(initial={'cellphone': ''})
        
        context = {
            'cart': len(cart),
            'form': form,
        }

        return render(request, 'checkout.html', context)

    def post(self, request):
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
        else:
            cart = []

        foods = Food.objects.filter(pk__in=cart)
        total = CartView().get_total(cart)

        form = CheckoutForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.total_price = total
            instance.save()
            for food in foods:
                instance.food.add(food)
            instance.save()
        context = {
            'cart': len(cart),
            'form': form
        }

        return render(request, 'checkout.html', context)


class SigninView(View):

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        context = {
            'form': form,
        }
        return render(request, 'signin.html', context)


    
    def get(self, request):
        form = LoginForm(request)
        if request.user.is_authenticated:
            return redirect('/')
        context = {
            'form': form,
        }

        return render(request, 'signin.html', context)



class SignupView(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success! Registered successfully")
            return redirect('/')
        
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

    def get(self, request):
        form = RegisterForm()
        if request.user.is_authenticated:
            return redirect('/')

        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/')

