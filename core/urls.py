from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('add-expense/', views.add_expense, name='add_expense'),
    path('user-expenses/<int:user_id>/', views.get_user_expenses, name='get_user_expenses'),
    path('user-balances/<int:user_id>/', views.get_user_balances, name='get_user_balances'),
]
