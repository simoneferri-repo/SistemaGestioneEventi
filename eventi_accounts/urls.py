from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, EditUserView
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profilo/edit/', EditUserView.as_view(), name='modifica_profilo'),
    path(
        'profilo/cambia-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='modifica_password.html',
            success_url=reverse_lazy('password_change_done')
        ),
        name='password_change'
    ),

    # 2. Pagina di conferma successo
    path(
        'profilo/cambia-password/fatto/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='modifica_password_confermata.html'
        ),
        name='password_change_done'
    ),
]