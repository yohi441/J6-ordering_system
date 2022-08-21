
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView
from ordering.models import Food
from django.db.models import Q
from collections import Counter



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

    def total(self, list_items):
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

        foods = Food.objects.filter(pk__in=self.request.session['cart'])
        c = Counter(cart)
        total = self.total(cart)
        context = {
            'cart': len(cart),
            'foods': foods,
            'counter': dict(c),
            'total': total
        }
        return render(request, 'cart.html', context)




class DetailView(DetailView):
    template_name = "detail_full_view.html"
    model = Food
    context_object_name = "food"