from django import forms
from transportapp.models import ReasearchStand,ReasearchStand_detail,Transpor_Type,Route,Traffic_Stop,Reasearcher,Reasearch,Reasearch_detail,Season,Day_Type,Time_of_Day,Result

class ChooseRouteForm(forms.ModelForm):

    class Meta:
        model=Reasearch
        fields = "__all__"

class ChooseStopForm(forms.ModelForm):
    class Meta:
        model=ReasearchStand
        fields = "__all__"


class ResearchDetailForm(forms.ModelForm):

    class Meta:
        model = Reasearch_detail
        fields = ('numberin', 'numberout', 'traffic_stop', 'reasearch')



class ResearchDetailStandForm(forms.ModelForm):

    class Meta:
        model = ReasearchStand_detail
        fields = "__all__"
