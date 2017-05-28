from django.shortcuts import render, render_to_response
from transportapp.forms import ResultForm, ChooseRouteForm, ResearchDetailForm, ChooseStopForm, ResearchDetailStandForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from transportapp.models import Check, Reasearch, Traffic_Stop, Reasearch_detail, ReasearchStand, ReasearchStand_detail, Route, Transpor_Type
#from django.core.context_processors import csrf
import plotly
import matplotlib.pyplot as plt
import numpy as np



def about(request):
    return render(request, 'transportapp/about.html')

def index(request):
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
            return redirect('show_res', pk=post.pk)
    else:
        form = ResultForm()
    return render(request, 'transportapp/home.html', {'form': form})

def show_res(request, pk):
    res = Check.objects.get(pk=pk)
    transtype = Route.objects.get(name=res.route).transport_type
    maxpeople = Transpor_Type.objects.get(name=transtype).maxpeople
    traffic_stops = Traffic_Stop.objects.filter(route=res.route).all()
    traffic_stops_count = Traffic_Stop.objects.filter(route=res.route).count()
    print(maxpeople)
# season month detect
    if res.season == 'S':
        minmon = 5
        maxmon = 8
    elif res.season == 'W':
        minmon = 11
        maxmon = 2
    elif res.season == 'Sp':
        minmon = 2
        maxmon = 5
    else:
        minmon = 8
        maxmon = 11
# type of day detect
    if res.daytype == 'W':
        minday = -1
        maxday = 3
    elif res.daytype == 'F':
        minday = 3
        maxday = 4
    else:
        minday = 4
        maxday = 6

    resstand=ReasearchStand.objects.filter(route=res.route).filter(month__gt=minmon).filter(month__lte=maxmon).filter(weekday__gt=minday).filter(weekday__lte=maxday).filter(date__gt=res.timestart).filter(date__lte=res.timeend).all()
    resgo=Reasearch.objects.filter(route=res.route).filter(month__gt=minmon).filter(month__lte=maxmon).filter(weekday__gt=minday).filter(weekday__lte=maxday).filter(date__gt=res.timestart).filter(date__lte=res.timeend).all()
    check = True
# we have enought info for research
    if resstand and resgo:

        traffic_list=[]
        traffic_time_list=[]

        # check reasearchs for "in"
        for rescount in resgo:
            if Reasearch_detail.objects.filter(reasearch=rescount).count() == traffic_stops_count:
                for ts in traffic_stops:
                    stoplist = Reasearch_detail.objects.filter(reasearch=rescount).filter(traffic_stop=ts).all()
                    for stop in stoplist:
                        traffic_list_uno=[]
                        traffic_list_uno.append(stop.reasearch)
                        traffic_list_uno.append(stop.traffic_stop)
                        traffic_list_uno.append(stop.numberin)
                        traffic_list_uno.append(stop.numberout)
                        traffic_list.append(traffic_list_uno)
            else:
                print('no go traffic stops')

        #check research for "out"
        for rescount in resstand:
            for ts in traffic_stops:
                stoptimelist = ReasearchStand_detail.objects.filter(reasearch=rescount).filter(traffic_stop=ts).all()
                for stop in stoptimelist:
                    traffic_time_list_uno=[]
                    traffic_time_list_uno.append(stop.traffic_stop)
                    traffic_time_list_uno.append(stop.numbercome/stop.timewait)
                    traffic_time_list_uno.append(stop.timewait)
                    traffic_time_list.append(traffic_time_list_uno)
        intensity_medians=[]
        try:

            for ts in traffic_stops:
                intensitymedian = 0
                timemedian = 0
                count = 0
                intensity_medians_uno=[]
                for i in range(len(traffic_time_list)):
                    if traffic_time_list[i][0] == ts:
                        intensitymedian += traffic_time_list[i][1]
                        timemedian += traffic_time_list[i][2]
                        count += 1
                if count == 0:
                    print('no stand traffic stops')
                else:
                    intensity_medians_uno.append(ts)
                    intensity_medians_uno.append((intensitymedian/count))
                    intensity_medians_uno.append(timemedian/count)
                intensity_medians.append(intensity_medians_uno)





        # calculate probability of exit for all elements in list "traffic_list"
            probability=[]
            peopleintransport = 0
            probabilityofexit = 0
            for i in range(len(traffic_list)):
                probability_uno=[]
                if i==0:
                    probabilityofexit = traffic_list[i][3]/traffic_list[i][2]
                else:
                    probabilityofexit = traffic_list[i][3]/peopleintransport

                print("profex")
                print(probabilityofexit)
                peopleintransport += traffic_list[i][2]-traffic_list[i][3]
                probability_uno.append(traffic_list[i][1])
                probability_uno.append(probabilityofexit)
                probability.append(probability_uno)



        # calculate median probability for every traffic stop on the Route
            probability_medians=[]
            for ts in traffic_stops:
                probabilityofexitmedian = 0
                count = 0
                probability_medians_uno=[]
                for i in range(len(probability)):
                    if probability[i][0] == ts:
                        probabilityofexitmedian += probability[i][1]
                        count += 1
                probability_medians_uno.append(ts)
                probability_medians_uno.append(probabilityofexitmedian/count)
                probability_medians.append(probability_medians_uno)
            peoplenow = 0
            count = 0
            statistic = []
            foradmin =[]
            i=0
            for ts in traffic_stops:
                foradmin_uno=[]
                foradmin_uno.append("Stop " + ts.name )
                foradmin_uno.append("Probability of exit : " + str(probability_medians[i][1]*100) + " %")
                foradmin_uno.append("Intensity of coming : " + str(intensity_medians[i][1]*60) + " in hour")
                foradmin.append(foradmin_uno)
                i+=1
            statistic.append(foradmin)

            for ts in traffic_stops:
                peoplenow += intensity_medians[count][1]*intensity_medians[count][2] - probability_medians[count][1]*peoplenow
                if peoplenow > maxpeople :
                    situation = 'DANGER'
                else:
                    situation = 'OK'
                statistic_uno=[]
                statistic_uno.append(ts.name)
                statistic_uno.append(peoplenow)
                statistic_uno.append(situation)
                #statistic.append(statistic_uno)
                count += 1

            content = statistic
        except:
            check=False

#not enought info for research
    else:
        a = "WE HAVE NOT ENOUGHT DATE"
        content =[]
        content.append(a)
    if check==False:
        a = "WE HAVE NOT ENOUGHT DATE"
        content =[]
        content.append(a)



    return render(request, 'transportapp/show_res.html', {'content': content})

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def add_detail_stand(request, pk):
    reasearch = ReasearchStand.objects.get(pk=pk)
    if request.method == "POST":
        form=ResearchDetailStandForm(initial = {'reasearch': reasearch })
        form = ResearchDetailStandForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.save()
            return redirect('index')
    else:
        form = ResearchDetailStandForm()
    return render(request, 'transportapp/add_detail_stand.html', {'form': form})
