from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('take/<int:id>',views.takeQuiz,name="take"),
    path('results/',views.results,name="results"),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/',views.DownloadPDF.as_view(), name="pdf_download"),
    path('show/',views.show, name="show"),
]
