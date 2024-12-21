from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from restaurant.models import Dish
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from . import models
from .forms import DishFilterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm

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
    
