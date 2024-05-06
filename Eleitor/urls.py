from django.urls import path
from .views import EleitorView, VerifyEleitorView

urlpatterns = [
    path('', EleitorView.as_view()),
    path('verify', VerifyEleitorView.as_view()),
]