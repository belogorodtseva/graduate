from django.shortcuts import render, render_to_response
from transportapp.forms import ChooseRouteForm, ResearchDetailForm, ChooseStopForm, ResearchDetailStandForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from transportapp.models import Reasearch, Traffic_Stop, Reasearch_detail, ReasearchStand, ReasearchStand_detail
#from django.core.context_processors import csrf


def index(request):
    return render(request, 'transportapp/home.html')

def about(request):
    return render(request, 'transportapp/about.html')

def show(request):
    return render(request, 'transportapp/show.html')


def add(request):
    if request.method == "POST":
        form = ChooseRouteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
            return redirect('add_detail', pk=post.pk)
    else:
        form = ChooseRouteForm()
    return render(request, 'transportapp/add.html', {'form': form})

def add_detail(request, pk):
    reasearch = Reasearch.objects.get(pk=pk)
    traffic_stops = Traffic_Stop.objects.filter(route=reasearch.route).all()
    forms_list = []
    for traffic_stop in traffic_stops:
        form=ResearchDetailForm(initial = {'reasearch': reasearch, 'traffic_stop': traffic_stop})
        forms_list.append(form)

    if request.method == "POST":
        form = ResearchDetailForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
    else:
        form = ResearchDetailForm()
    return render(request, 'transportapp/add_detail.html', {'forms': forms_list})

def add_stand(request):
    if request.method == "POST":
        form = ChooseStopForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
            return redirect('add_detail_stand', pk=post.pk)
    else:
        form = ChooseStopForm()
    return render(request, 'transportapp/add_stand.html', {'form': form})

def add_detail_stand(request, pk):
    reasearch = ReasearchStand.objects.get(pk=pk)
    form=ResearchDetailForm(initial = {'reasearch': reasearch })
    if request.method == "POST":
        form = ResearchDetailStandForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
    else:
        form = ResearchDetailStandForm()
    return render(request, 'transportapp/add_detail_stand.html', {'form': form})
