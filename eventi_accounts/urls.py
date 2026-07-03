from django.urls import path

from .views import SignUpView, EditUserView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profilo/edit/', EditUserView.as_view(), name='modifica_profilo'),
]