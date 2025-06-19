from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Exists, OuterRef, Count, Q
from django.http import JsonResponse

from .models import Quote, Like, Comment, SubComment
from .forms import CommentForm, SubCommentForm



class IndexView(generic.TemplateView):
    template_name = 'myApp/index.html'


class QuoteListView(LoginRequiredMixin, generic.ListView):
    model = Quote
    template_name = 'myApp/quote_list.html'
    context_object_name = 'quotes'

    def get_queryset(self):
        user = self.request.user
        queryset = Quote.objects.annotate(
            liked=Exists(Like.objects.filter(user=user, quote=OuterRef('pk')))).annotate(
                comments_num=(Count('comments', distinct=True) + Count('comments__sub_comments', distinct=True)))
        return queryset



def quote_detail(request, pk):
    # Get the quote and related comments
    quote = get_object_or_404(Quote, pk=pk)
    comments = Comment.objects.filter(quote=quote)

    # Initialize empty forms
    comment_form = CommentForm()
    subcomment_form = SubCommentForm()

    return render(request, 'myApp/quote_detail.html', {
        'quote': quote,
        'comments': comments,
        'comment_form': comment_form,
        'subcomment_form': subcomment_form
    })

def add_comment(request, pk):
    # Get the quote to associate the comment
    quote = get_object_or_404(Quote, pk=pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.quote = quote
            new_comment.publisher = request.user
            new_comment.save()
            return redirect('myApp:quote_detail', pk=quote.pk)  # Redirect to the same page after saving the comment

    return redirect('myApp:quote_detail', pk=quote.pk)  # Redirect back to the quote detail if the form isn't valid

def add_subcomment(request, pk, comment_id):
    # Get the quote and comment to associate the subcomment
    quote = get_object_or_404(Quote, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        subcomment_form = SubCommentForm(request.POST)
        if subcomment_form.is_valid():
            new_subcomment = subcomment_form.save(commit=False)
            new_subcomment.comment = comment
            new_subcomment.quote = quote
            new_subcomment.publisher = request.user
            new_subcomment.save()
            return redirect('myApp:quote_detail', pk=quote.pk)  # Redirect to the same page after saving the subcomment

    return redirect('myApp:quote_detail', pk=quote.pk)  # Redirect back if the form isn't valid



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
    success_url = reverse_lazy('myApp:quote_list')

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


def like(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    if request.method == 'POST':
        like_object = Like.objects.filter(user=request.user, quote=quote)

        # Toggle like status
        if like_object.exists():
            like_object.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, quote=quote)
            liked = True

        # Return a JSON response with the new like status
        return JsonResponse({
            'liked': liked,
            'like_count': quote.count_likes(),  # You can modify this to show the total like count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
