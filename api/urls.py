from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, AddExpenseAPIView, UserExpensesAPIView, BalancesAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('expenses/add/', AddExpenseAPIView.as_view(), name='add_expense_api'),
    path('expenses/user/<int:user_id>/', UserExpensesAPIView.as_view(), name='user_expenses_api'),
    path('balances/', BalancesAPIView.as_view(), name='balances_api'),
]
