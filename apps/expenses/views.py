from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from datetime import datetime
from django.db.models import Sum

def index(request):
    meses = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]

    hoy = datetime.today()
    mes = int(request.GET.get('mes', hoy.month))
    anio = int(request.GET.get('anio', hoy.year))

    gastos_agrupados = (
        Expense.objects
        .filter(date__month=mes, date__year=anio)
        .values('type__name')
        .annotate(total=Sum('total'))
        .order_by('type__name')
    )

    return render(request, 'expenses/index.html', {
        'gastos_agrupados': gastos_agrupados,
        'mes_actual': f"{meses[mes - 1][1]} {anio}",
        'meses': meses,
        'anios': list(range(hoy.year - 5, hoy.year + 1)),
        'mes_actual_num': mes,
        'anio_actual': anio
    })

def create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses:index') 
    else:
        form = ExpenseForm()

    return render(request, 'expenses/form.html', {'form': form})


def detail(request, pk):
    gasto = Expense.objects.get(pk=pk)
    return render(request, 'expenses/detail.html', {'gasto': gasto})

def detail_group(request, tipo):
    gastos = Expense.objects.filter(type__name=tipo).order_by('-date')
    return render(request, 'expenses/detail_group.html', {
        'gastos': gastos,
        'tipo': tipo
    })