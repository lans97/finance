from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.utils import timezone

from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm

from collections import defaultdict

def index(request):
    now = timezone.now()
    current_year = now.year

    income_total = Transaction.objects.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense_total = Transaction.objects.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

    # Expenses by category
    category_data = (
        Transaction.objects
        .filter(type='EXPENSE')
        .values('category__name', 'category__color_hex')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Monthly totals
    monthly_data = (
        Transaction.objects
        .filter(date__year=current_year)
        .values('date__month', 'type')
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )

    # monthly_data = [{ 'date__month': 1, 'type': 'INCOME', 'total': 1000 }, ...]
    monthly_balance = defaultdict(lambda: {'income': 0, 'expense': 0})

    for item in monthly_data:
        month = item['date__month']
        if item['type'] == 'INCOME':
            monthly_balance[month]['income'] = item['total'] or 0
        else:
            monthly_balance[month]['expense'] = item['total'] or 0

    balance_data = [
        {'month': m, 'balance': monthly_balance[m]['income'] - monthly_balance[m]['expense']}
        for m in range(1, 13)
    ]

    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'category_data': list(category_data),
        'monthly_data': list(monthly_data),
        'balance_data': list(balance_data),
        'now': now,
    }
    return render(request, 'dashboard/index.html', context)

# --- Transactions ---
class TransactionListView(ListView):
    model = Transaction
    template_name = 'crud/transactions/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-date']

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'crud/transactions/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'crud/transactions/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'crud/transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

# --- Categories ---
class CategoryListView(ListView):
    model = Category
    template_name = 'crud/categories/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'crud/categories/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'crud/categories/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'crud/categories/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
