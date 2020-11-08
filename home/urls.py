from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="home"),
    path('<int:id>/', views.detail, name='detail'),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('ordered_detail/', views.ordered, name='ordered'),

    path('count_click', views.count_click, name='count_click'),
    path('count_like', views.count_like, name='count_like'),
    path('count_dislike', views.count_dislike, name='count_dislike'),
    path('statistical', views.statistical, name='statistical'),
    path('delete', views.delete_product, name='delete_product'),
    path('buy_product', views.buy_product, name='buy_product'),

]