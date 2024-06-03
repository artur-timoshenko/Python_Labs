from django.shortcuts import render
from django.http import HttpResponse
from .models import Player
from .forms import UserForm

def index(request):
    form = UserForm(request.POST or None, initial={'team_id': 0})
    id = 0
    if form.is_valid():
        id = form.cleaned_data.get("team_id")
    data = list(Player.objects.all().filter(team_id=int(id)))
    print(data)
    context = {
        'data': data,
        'form': form
    }
    return render(request, 'index.html', context)
    # return HttpResponse("aaa")
