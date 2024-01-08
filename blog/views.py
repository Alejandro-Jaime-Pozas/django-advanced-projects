from django.shortcuts import render, get_object_or_404

from .models import Post


# Create your views here.

# include a start page w only the 3 latest posts
def starting_page(request):
    latest_posts = Post.objects.all().order_by('-date')[:3] # order by desc date '-date'; [-1] does not work in this django case for lists; django recognizes this as a SQL query, so performance is optimized and doesn't search whole list, instead it filters by WHERE clause to get 3 latest posts
    return render(request, 'blog/index.html', {
        'posts': latest_posts
    })


# include an all posts page that shows all posts
def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/all-posts.html', {
        'all_posts': all_posts
    })


# include the post detail including its content
def post_detail(request, slug):
    # identified_post = Post.objects.get(slug=slug)
    identified_post = get_object_or_404(Post, slug=slug) # get_404 gets an object, then with condition specified
    return render(request, 'blog/post-detail.html', {
        'post': identified_post,
        'post_tags': identified_post.tags.all() # now this is a query list
    })