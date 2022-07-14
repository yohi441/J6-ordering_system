
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from ordering.models import Food
from django.db.models import Q



class IndexView(View):

    def get(self, request):
        bests = Food.objects.filter(status="Best Seller")[:1]
        foods = Food.objects.exclude(Q(status="Best Seller")|Q(status="Out Of Stock"))
        if 'cart' in self.request.session: 
            cart = self.request.session['cart']
        else:
            cart = []
        
        context = {
            'foods': foods,
            'bests': bests,
            'cart': len(cart)
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
        context = {
            'cart': len(cart)
        }

        return render(request, 'service.html', context)


class ContactView(View):

    def get(self, request):
        if 'cart' in self.request.session: 
            cart = self.request.session['cart']
        else:
            cart = []
        context = {
            'cart': len(cart)
        }

        return render(request, 'contact.html', context)

class AddtocartView(View):

    def get(self, request, pk):
        

        if 'cart' in self.request.session:
            self.request.session['cart'].append(pk)

        else:
            self.request.session['cart'] = [pk]

        self.request.session.modified = True

        print(request.session['cart'])

        return redirect(reverse('index'))


class CartView(View):

    def get(self, request):
        if 'cart' in self.request.session: 
            cart = self.request.session['cart']
        else:
            cart = []

        foods = Food.objects.filter(pk__in=self.request.session['cart'])
        context = {
            'cart': len(cart),
            'foods': foods
        }
        return render(request, 'cart.html', context)
