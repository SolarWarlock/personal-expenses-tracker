from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Account, Category, Expense, Transfer


class FinancialLogicTests(TestCase):
    def setUp(self):
        # setUp запускается перед каждым тестом.
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account = Account.objects.create(
            user=self.user,
            name='Тестовая карта',
            balance=Decimal('1000.00')
        )
        self.category = Category.objects.create(name='Кофе')

    def test_expense_creation_deducts_balance(self):
        # Действие: расход на 200 рублей
        Expense.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=Decimal('200.00'),
            date='2026-04-10'
        )

        # Обновление: извлечение счета из базы заново,
        self.account.refresh_from_db()

        # Проверка
        self.assertEqual(self.account.balance, Decimal('800.00'))

    def test_transfer_updates_both_balances(self):
        # 1. Второй счет специально для этого теста
        account2 = Account.objects.create(
            user=self.user,
            name='Копилка',
            balance=Decimal('500.00')
        )

        # 2. Переводим 300 рублей с тестовой карты (1000) на копилку (там 500)
        Transfer.objects.create(
            user=self.user,
            from_account=self.account,
            to_account=account2,
            amount=Decimal('300.00'),
            date='2026-04-10'
        )

        # Достаем оба счета из базы заново, чтобы увидеть работу сигналов
        self.account.refresh_from_db()
        account2.refresh_from_db()

        # На первом счете должно остаться 700, на втором — стать 800
        self.assertEqual(self.account.balance, Decimal('700.00'))
        self.assertEqual(account2.balance, Decimal('800.00'))