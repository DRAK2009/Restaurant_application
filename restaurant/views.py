from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.http import require_POST

from . import models
from .forms import DishFilterForm, CartAddDishForm
from .cart import Cart
from restaurant.models import Dish

def index(request):
    context = {
        "render_string": "Hello, world!"
    }
    return render(request, template_name="restaurant/index.html", context=context)

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomLoginView(LoginView):
    template_name = 'restaurant/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    template_name = 'restaurant/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class DishListView(ListView):
    model = models.Dish
    context_object_name = "dishes"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category", "")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DishFilterForm(self.request.GET)
        return context

class DishDetailView(DetailView):
    model = models.Dish
    context_object_name = "dish"

@require_POST
def CartAdd(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartRemove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.remove(dish)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddDishForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/detail.html', {'cart': cart})
