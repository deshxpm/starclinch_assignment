from core.models import ExpenseSplit, Balance

def calculate_balances():
    balances = {}

    expense_splits = ExpenseSplit.objects.all()
    for split in expense_splits:
        user_id = split.user_id
        amount_owed = split.amount_owed

        if user_id in balances:
            balances[user_id] += amount_owed
        else:
            balances[user_id] = amount_owed

    balance_objects = []
    for user_id, amount in balances.items():
        balance_objects.append(Balance(user_id=user_id, amount=amount))

    return balance_objects
