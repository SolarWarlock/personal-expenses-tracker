import django_filters
from django import forms
from .models import Expense, Account, Category


class ExpenseFilter(django_filters.FilterSet):
    # Явное определение полей для фильтрации по диапазону дат
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Начиная с даты',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Заканчивая датой',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Expense
        fields = ['account', 'category']

    def __init__(self, *args, **kwargs):
        # Извлечение объекта request для получения текущего пользователя
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            # Ограничение списка счетов только счетами авторизованного пользователя
            self.filters['account'].queryset = Account.objects.filter(user=request.user)