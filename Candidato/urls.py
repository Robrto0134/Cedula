from django.urls import path
from .views import CandidatoView

urlpatterns = [
    path('', CandidatoView.as_view()),
]