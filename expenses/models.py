from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts', verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название счета")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'),
                                  verbose_name="Текущий баланс")

    def __str__(self):
        return f"{self.name} ({self.balance} ₽)"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses',
                                verbose_name="Счет списания")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    description = models.TextField(blank=True, verbose_name="Описание")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f"{self.amount} ₽ - {self.category.name}"


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_out',
                                     verbose_name="Счет списания")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfers_in',
                                   verbose_name="Счет пополнения")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма перевода")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f"Перевод {self.amount} ₽: {self.from_account.name} -> {self.to_account.name}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    limit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Лимит на месяц")

    def __str__(self):
        return f"Бюджет: {self.category.name} - {self.limit} ₽"