from django.shortcuts import render, redirect, get_object_or_404
from .models import Momento
from .forms import MomentoForm

def index(request):
    if request.method == 'POST':
        form = MomentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MomentoForm()

    # AQUÍ ESTÁ LA MAGIA: 'fecha' ordena de la más antigua a la más reciente.
    # Si quisieras al revés sería '-fecha'.
    momentos = Momento.objects.all().order_by('fecha') 
    
    context = {
        'momentos': momentos,
        'form': form
    }
    return render(request, 'index.html', context)

def eliminar_momento(request, momento_id):
    momento = get_object_or_404(Momento, id=momento_id)
    momento.delete()
    return redirect('home')

def editar_momento(request, momento_id):
    momento = get_object_or_404(Momento, id=momento_id)
    if request.method == 'POST':
        form = MomentoForm(request.POST, request.FILES, instance=momento)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')