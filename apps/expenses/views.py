from django.shortcuts import render, redirect
from .forms import ExpenseForm

def index(request):
    return render(request, 'expenses/index.html')

def create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses:index') 
    else:
        form = ExpenseForm()

    return render(request, 'expenses/form.html', {'form': form})
