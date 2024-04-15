from django.contrib import admin
from .models import UserProfile, Expense, Balance, ExpenseSplit

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'expense_type')

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')

class ExpenseSplitAdmin(admin.ModelAdmin):
    list_display = ('expense', 'user', 'amount_owed')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(ExpenseSplit, ExpenseSplitAdmin)
