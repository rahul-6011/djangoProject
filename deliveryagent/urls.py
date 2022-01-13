from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('home_d',views.home_d,name = "home_d"),
    path('accpetd/<int:id>',views.accpetd,name = "accpetd"),
    path('delivd/<int:id>',views.delivd,name = "delivd"),
    path('retrn_reqd',views.retrn_reqd,name = "retrn_reqd"),
    path('accptd_rtn/<int:id>',views.accptd_rtn,name = "accptd_rtn"),
    path('delivd_rtn/<int:id>',views.delivd_rtn,name = "delivd_rtn"),
]