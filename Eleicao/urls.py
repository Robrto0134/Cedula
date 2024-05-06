from django.urls import path
from .views import EleicaoView, VoteEleicaoView, ResultsEleicaoView

urlpatterns = [
    path('', EleicaoView.as_view()),
    path('vote', VoteEleicaoView.as_view()),
    path('results', ResultsEleicaoView.as_view()),


]