from django.contrib import admin


# Register your models here.
from transportapp.models import ReasearchStand,ReasearchStand_detail,Transpor_Type,Route,Traffic_Stop,Reasearch,Reasearch_detail,Check

admin.site.register(Transpor_Type)
admin.site.register(Traffic_Stop)
admin.site.register(Reasearch)

admin.site.register(Reasearch_detail)
admin.site.register(Check)
admin.site.register(Route)
admin.site.register(ReasearchStand)
admin.site.register(ReasearchStand_detail)
