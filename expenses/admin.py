from django.contrib import admin
from .models import Account, Category, Expense, Transfer, Budget

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'account', 'user', 'date')
    list_filter = ('date', 'category', 'account')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('amount', 'from_account', 'to_account', 'user', 'date')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'limit', 'user')