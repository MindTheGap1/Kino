from django.urls import path, include

from . import views

app_name = 'orders'
urlpatterns = [
	path('checkout/', views.checkout, name='checkout'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_history/', views.order_history, name='order_history'),
    path('watch/<int:movie_id>', views.watch, name='watch'),
]