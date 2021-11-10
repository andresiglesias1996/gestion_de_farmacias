from django.urls import path
from .views import SignUpView, RecuperarPassword


urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('recuperar_password/', RecuperarPassword.as_view(), name="recuperar_password"),
]
