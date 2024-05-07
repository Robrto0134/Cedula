from django.urls import path
from .views import MesarioView, VerifyMesarioView, ApproveMesarioView, DenyMesarioView

urlpatterns = [
    path('', MesarioView.as_view()),
    path('verify', VerifyMesarioView.as_view()),
    path('approve', ApproveMesarioView.as_view()),
    path('deny', DenyMesarioView.as_view()),
    
]
