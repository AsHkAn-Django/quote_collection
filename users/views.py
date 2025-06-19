from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



class UserCreateView(generic.CreateView):
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')