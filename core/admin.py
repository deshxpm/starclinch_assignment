from django.contrib import admin
from .models import UserProfile, Expense, Balance, ExpenseSplit

admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(Balance)
admin.site.register(ExpenseSplit)
