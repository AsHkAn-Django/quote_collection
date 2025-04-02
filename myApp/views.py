from django.views import generic  
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Exists, OuterRef

from .forms import LikeForm
from .models import Quote, Like



class IndexView(generic.TemplateView):
    template_name = 'myApp/index.html'


class QuoteListView(LoginRequiredMixin, generic.ListView):
    model = Quote
    template_name = 'myApp/quote_list.html'
    context_object_name = 'quotes'
    
    def get_queryset(self):
        user = self.request.user
        queryset = Quote.objects.annotate(liked=Exists(Like.objects.filter(user=user, quote=OuterRef('pk'))))
        return queryset    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LikeForm
        return context
    


class QuoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Quote
    template_name = 'myApp/quote_detail.html'


class QuoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Quote
    template_name = 'myApp/quote_edit.html'
    fields = ['body', 'author']

    def test_func(self):
        obj = self.get_object()
        return obj.publisher == self.request.user


class QuoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Quote
    template_name = 'myApp/quote_delete.html'
    success_url = reverse_lazy('quote_list')

    def test_func(self):
        obj = self.get_object()
        return obj.publisher == self.request.user


class QuoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Quote
    template_name = "myApp/quote_new.html"
    fields = ['body', 'author']
    
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'


def like(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    
    if request.method == 'POST':
        like_object = Like.objects.filter(user=request.user, quote=quote)
        if like_object.exists():
            like_object.delete()
        else:
            form = LikeForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.quote = quote
                form.save()         
    return redirect('quote_list')