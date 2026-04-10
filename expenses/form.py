from django import forms
from .models import Expense, Transfer, Budget, Account


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['account', 'category', 'amount', 'date', 'description']
        widgets = {
            # Использование HTML5 виджета для вызова нативного календаря в браузере
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Уменьшение высоты поля ввода текста
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Безопасное извлечение пользователя из аргументов инициализации формы
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['from_account', 'to_account', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # фильтрация для обоих списков выбора счетов
            user_accounts = Account.objects.filter(user=user)
            self.fields['from_account'].queryset = user_accounts
            self.fields['to_account'].queryset = user_accounts

    def clean(self):
        # Расширение стандартной валидации формы для проверки бизнес-логики
        cleaned_data = super().clean()
        from_account = cleaned_data.get('from_account')
        to_account = cleaned_data.get('to_account')

        # Блокировка транзакций, где счет списания и зачисления совпадают
        if from_account and to_account and from_account == to_account:
            raise forms.ValidationError("Счета списания и пополнения не могут совпадать.")

        return cleaned_data


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit']