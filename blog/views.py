from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post
from .forms import CommentForm


# Create your views here.

# include a start page w only the 3 latest posts
class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post 
    ordering = ['-date', ] # use ordering field to order the list of data '-' means desc order
    context_object_name = 'posts' # change name to readable for use in template

    def get_queryset(self): # to overwrite the default queryset
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# include a start page w only the 3 latest posts
def starting_page(request):
    latest_posts = Post.objects.all().order_by('-date')[:3] # order by desc date '-date'; [-1] does not work in this django case for lists; django recognizes this as a SQL query, so performance is optimized and doesn't search whole list, instead it filters by WHERE clause to get 3 latest posts
    return render(request, 'blog/index.html', {
        'posts': latest_posts
    })

    
# include an all posts page that shows all posts
class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post 
    ordering = ['-date']
    context_object_name = 'all_posts'

# include an all posts page that shows all posts
def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/all-posts.html', {
        'all_posts': all_posts
    })

    
# include the post detail including its content
class SinglePostView(DetailView): # this Detail view auto raises error if object not found and takes a slug as a field
    template_name = 'blog/post-detail.html'
    model = Post 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tags.all() # to get access to a single post's fields
        context['comment_form'] = CommentForm() # to create instance of a form based on comment model that you can then access within the template
        return context

# include the post detail including its content
def post_detail(request, slug):
    # identified_post = Post.objects.get(slug=slug)
    identified_post = get_object_or_404(Post, slug=slug) # get_404 gets an object, then with condition specified
    return render(request, 'blog/post-detail.html', {
        'post': identified_post,
        'post_tags': identified_post.tags.all() # now this is a query list, need this in order to get relationships for models
    })