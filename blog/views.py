from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.

def starting_page(request):
    latest_posts = Post.objects.all().order_by('-date')[:3] # order by desc date; [-1] does not work in this django case
    return render(request, 'blog/index.html', {
        'posts': latest_posts
    })


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/all-posts.html', {
        'all_posts': all_posts
    })


def post_detail(request, slug):
    # identified_post = Post.objects.get(slug=slug)
    identified_post = get_object_or_404(Post, slug=slug) # get_404 gets an object, then with condition specified
    return render(request, 'blog/post-detail.html', {
        'post': identified_post,
        'post_tags': identified_post.tags.all() # now this is a query list
    })