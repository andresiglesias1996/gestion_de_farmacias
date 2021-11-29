from django.urls import path
from .views import SignUpView, RecuperarPassword, MiLoginView, RegistroExitoso


urlpatterns = [
    path('login/', MiLoginView.as_view(), name="login"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('recuperar_password/', RecuperarPassword.as_view(), name="recuperar_password"),

    #path('registro_exitoso/', RegistroExitoso.as_view(), name="registro_exitoso"),
]
