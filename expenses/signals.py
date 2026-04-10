from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Expense, Transfer


# Сигнал: когда создаётся новый расход
@receiver(post_save, sender=Expense)
def update_balance_on_expense_save(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            account = instance.account
            account.balance -= instance.amount
            account.save()


# Сигнал: когда удаляется расход
@receiver(post_delete, sender=Expense)
def update_balance_on_expense_delete(sender, instance, **kwargs):
    with transaction.atomic():
        account = instance.account
        account.balance += instance.amount
        account.save()


# Сигнал: создан перевод
@receiver(post_save, sender=Transfer)
def update_balance_on_transfer_save(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            from_acc = instance.from_account
            to_acc = instance.to_account

            from_acc.balance -= instance.amount
            to_acc.balance += instance.amount

            from_acc.save()
            to_acc.save()


# Сигнал: откат операции
@receiver(post_delete, sender=Transfer)
def update_balance_on_transfer_delete(sender, instance, **kwargs):
    with transaction.atomic():
        from_acc = instance.from_account
        to_acc = instance.to_account

        from_acc.balance += instance.amount
        to_acc.balance -= instance.amount

        from_acc.save()
        to_acc.save()