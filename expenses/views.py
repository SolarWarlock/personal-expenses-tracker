from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from decimal import Decimal
from .models import Account, Expense, Transfer, Budget
from .form import ExpenseForm, TransferForm
from django.views.generic import TemplateView, CreateView, ListView
from .filters import ExpenseFilter


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получение текущего авторизованного пользователя
        user = self.request.user

        # Передача счетов пользователя в контекст шаблона
        context['accounts'] = Account.objects.filter(user=user)

        # Получение последних 5 расходов, отсортированных по дате
        context['recent_transfers'] = Transfer.objects.filter(user=user).order_by('-date')[:5]

        # Расчет прогресса по бюджетам для вывода предупреждений
        budgets = Budget.objects.filter(user=user)
        budget_data = []

        for budget in budgets:
            # Агрегатная функция Sum для подсчета всех трат по конкретной категории
            spent = Expense.objects.filter(
                user=user,
                category=budget.category
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # Логика проверки превышения 80% лимита
            is_warning = spent >= (budget.limit * Decimal('0.8'))

            budget_data.append({
                'category': budget.category.name,
                'limit': budget.limit,
                'spent': spent,
                'is_warning': is_warning
            })

        context['budgets'] = budget_data
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['accounts'] = Account.objects.filter(user=user)
        context['recent_expenses'] = Expense.objects.filter(user=user).order_by('-date')[:5]

        # 5 последних переводов
        context['recent_transfers'] = Transfer.objects.filter(user=user).order_by('-date')[:5]


        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    # Перенаправление на главную страницу после успешного сохранения
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        # Передача объекта пользователя внутрь формы для фильтрации QuerySet
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Автоматическая привязка текущего пользователя к создаваемому объекту
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransferCreateView(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'expenses/transfer_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HistoryView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/history.html'
    context_object_name = 'expenses'
    # Включение постраничного вывода (по 10 записей на страницу)
    paginate_by = 10

    def get_queryset(self):
        # Получение базового списка транзакций строго для текущего пользователя
        queryset = super().get_queryset().filter(user=self.request.user).order_by('-date')

        # Инициализация фильтра с передачей параметров get-запроса и объекта request
        self.filterset = ExpenseFilter(self.request.GET, queryset=queryset, request=self.request)

        # Возврат отфильтрованного QuerySet
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

