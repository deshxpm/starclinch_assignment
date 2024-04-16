from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Expense, Balance, UserProfile, ExpenseSplit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

def register(request):
    if request.method == 'POST':
        data = request.POST
        firstname  = data.get('first_name')
        lastname  = data.get('last_name')
        email = data.get('email').lower()
        phone = data.get('mobile')
        password = data.get('password')
        profile = UserProfile.objects.filter(Q(phone=phone)|Q(email = email)).first()
        if not profile:
            user = UserProfile.objects.create_user(first_name=firstname,last_name=lastname, password=password,phone=phone, email=email, username=email)
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def index(request):
    all_users = UserProfile.objects.filter(is_active=True)
    user_expenses = Expense.objects.filter(user=request.user)
    user_balances = Balance.objects.filter(user=request.user)
    user_share    = ExpenseSplit.objects.filter(expense__in=user_expenses)
    return render(request, 'index.html', {'all_users':all_users, 'user_expenses': user_expenses, 'user_balances': user_balances, 'user_share':user_share})

def update_balance(user_id, amount):
    try:
        user_balance = Balance.objects.get(user_id=user_id)
    except Balance.DoesNotExist:
        user_balance = Balance.objects.create(user_id=user_id, amount=amount)
    else:
        user_balance.amount += Decimal(amount)
        user_balance.save()


@login_required(login_url='/login/')
def add_expense(request):
    if request.method == 'POST':
        user_id = request.user.id #request.POST.get('user_id')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')
        participants_ids = request.POST.getlist('participants')
        if len(participants_ids) > 1000:
            return JsonResponse({'error': 'Maximum participants limit exceeded'}, status=400)
        
        try:
            amount = float(amount)
            if amount > 10000000:  # 1,00,00,000
                return JsonResponse({'error': 'Maximum amount limit exceeded'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        if not amount or not expense_type:
            return JsonResponse({'error': 'Amount and expense type are required'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        if expense_type == Expense.EQUAL:
            if not participants_ids:
                return JsonResponse({'error': 'At least one participant is required for EQUAL expense'}, status=400)

            expense = Expense.objects.create(
                user_id=user_id,
                amount=amount,
                expense_type=Expense.EQUAL
            )
            Balance.objects.create(
                    user_id=user_id,
                    # owes_to_id=user_id,
                    amount=amount
                )

            share = amount / (len(participants_ids) + 1)  # Including the user who paid
            for participant_id in participants_ids:
                user_profile = UserProfile.objects.get(id=participant_id)
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user_profile,  # Use the actual UserProfile object
                    amount_owed=share
                )
    
    ############################################################################################            
        elif expense_type == Expense.EXACT:
            amounts_owed = request.POST.getlist('exact_amount')
            
            payer_profile = UserProfile.objects.get(id=user_id)
        
            updated_balances = {}
            for user_id, amount in enumerate(amounts_owed, start=1):
                if user_id != user_id:
                    user_profile = UserProfile.objects.get(id=user_id)
                    payer_balance, _ = Balance.objects.get_or_create(user=payer_profile)
                    user_balance, _ = Balance.objects.get_or_create(user=user_profile)
                    payer_balance.amount -= float(amount)
                    user_balance.amount += float(amount)
                    payer_balance.save()
                    user_balance.save()
                    updated_balances[user_id] = payer_balance.amount


                
    ############################################################################    
        elif expense_type == Expense.PERCENT:
            participants = request.POST.getlist('participants')
            percentages = request.POST.getlist('percentages')
            print(request.POST,14545454)
            print(participants,111)
            print(percentages,222)
            if len(participants) != len(percentages):
                return JsonResponse({'error': 'Number of participants should match the number of percentages'}, status=400)

            total_percentage = sum(map(int, percentages))
            if total_percentage != 100:
                return JsonResponse({'error': 'Total percentage must be 100'}, status=400)
            
            update_balance(user_id, amount)
            expense = Expense.objects.create(
                user_id=user_id,
                amount=amount,
                expense_type=Expense.PERCENT
            )

            for participant, percentage in zip(participants, percentages):
                user_profile = UserProfile.objects.get(id=participant)
                amount_owed = (amount * (int(percentage) / 100))
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user_profile,
                    amount_owed=amount_owed
                )

                update_balance(participant, -amount_owed)
                update_balance(user_id, amount_owed)
            
        # return JsonResponse({'message': 'Expense added successfully'})
        return redirect('/')
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


@login_required(login_url='/login/')
def get_user_expenses(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    expenses = Expense.objects.filter(user=user)
    return JsonResponse({'expenses': expenses})

@login_required(login_url='/login/')
def get_user_balances(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    balances = Balance.objects.filter(user=user)
    return JsonResponse({'balances': balances})
