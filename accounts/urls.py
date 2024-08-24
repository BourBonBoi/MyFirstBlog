from django.urls import path, reverse_lazy
from .views import RegistrationView, CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),  # Укажите имя URL для главной страницы

]