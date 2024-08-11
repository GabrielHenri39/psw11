from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"), #  # type: ignore
    path('logar/',views.login,name='login'), # type: ignore
    path('sair/',views.logout,name='sair')
]