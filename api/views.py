from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import UserProfileSerializer
from core.models import Expense, Balance
from .serializers import ExpenseSerializer, BalanceSerializer
from .utils import calculate_balances

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class AddExpenseAPIView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserExpensesAPIView(APIView):
    def get(self, request, user_id):
        expenses = Expense.objects.filter(user_id=user_id)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

class BalancesAPIView(APIView):
    def get(self, request):
        balances = calculate_balances()
        print(balances,1111111111111)
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)