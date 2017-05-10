from django import forms
import datetime
from transportapp.models import Check,ReasearchStand,ReasearchStand_detail,Transpor_Type,Route,Traffic_Stop,Reasearch,Reasearch_detail
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets

class ChooseRouteForm(forms.ModelForm):

    class Meta:
        model=Reasearch
        fields = "__all__"


class ChooseStopForm(forms.ModelForm):
    class Meta:
        model=ReasearchStand
        fields = "__all__"

class ResultForm(forms.ModelForm):

    class Meta:
        model=Check
        fields = "__all__"
        widgets = {'timestart': forms.DateInput(attrs={'id': 'datetimepicker12'})}



class ResearchDetailForm(forms.ModelForm):

    class Meta:
        model = Reasearch_detail
        fields = ('numberin', 'numberout', 'traffic_stop', 'reasearch')



class ResearchDetailStandForm(forms.ModelForm):

    class Meta:
        model = ReasearchStand_detail
        fields = "__all__"
