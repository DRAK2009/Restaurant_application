from django.urls import path
from . import views

urlpatterns = [
    path('', views.DishListView.as_view(), name='dish-list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.DishDetailView.as_view(), name='dish-detail'),
    path(r'^$', views.CartDetail, name='CartDetail'),
    path(r'^remove/(?P<product_id>\d+)/$', views.CartRemove, name='CartRemove'),
    path(r'^add/(?P<product_id>\d+)/$', views.CartAdd, name='CartAdd'),
]
