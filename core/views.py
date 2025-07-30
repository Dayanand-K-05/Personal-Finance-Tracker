# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Transaction
from .forms import TransactionForm, CategoryForm # Import your new forms
from django.db.models import Sum
from django.contrib import messages # For displaying success/error messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard_view(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    user_categories = Category.objects.filter(user=request.user)

    # Calculate total income and expense for the current user
    total_income = user_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = user_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense

    context = {
        'transactions': user_transactions[:10], # Show last 10 transactions on dashboard
        'categories': user_categories,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user) # Pass the user to the form
        if form.is_valid():
            transaction = form.save(commit=False) # Don't save yet
            transaction.user = request.user # Assign the current user
            transaction.save() # Now save
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransactionForm(user=request.user) # Pass the user to the form for GET requests too
    return render(request, 'core/add_transaction.html', {'form': form})

@login_required
def manage_categories(request):
    user_categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, initial={'user': request.user}) # Pass user to initial for validation
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('manage_categories')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm() # Empty form for GET request
    return render(request, 'core/manage_categories.html', {'categories': user_categories, 'form': form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'Category "{category.name}" deleted successfully.')
    return redirect('manage_categories')

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
    return redirect('dashboard') # Or a view showing all transactions
