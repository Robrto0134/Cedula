from django.urls import path
from .views import MesarioView, VerifyMesarioView, ApproveMesarioView, DenyMesarioView, login_administrador, pagina_resultado

urlpatterns = [
    path('', MesarioView.as_view()),
    path('verify', VerifyMesarioView.as_view()),
    path('approve', ApproveMesarioView.as_view()),
    path('deny', DenyMesarioView.as_view()),
    path('login/', login_administrador, name='login_administrador'),
    path('resultado/', pagina_resultado, name='pagina_resultado'),
]
