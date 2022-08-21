from django.urls import path
from ordering import views



urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('service/', views.ServiceView.as_view(), name="service"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('add/to/cart/<int:pk>/', views.AddtocartView.as_view(), name="add_to_cart"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail-view"),
    path('delete/cart/item/<int:pk>/', views.DeleteItemInCartView.as_view(), name="delete-cart-item"),

]
