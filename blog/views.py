from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

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
class SinglePostView(View): # this Detail view auto raises error if object not found and takes a slug as a field
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False 
        return is_saved_for_later

    def get(self, request, slug): # slug is parameter passed through in the url request linked to this view
        post = Post.objects.get(slug=slug)
        # include context data for use in template
        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by("-id"),
            'saved_for_later': self.is_stored_post(request, post.id),
        }
        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST) # request.POST contains the user's submitted data
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid(): # check if requirements for form based on Comment model are met
            comment = comment_form.save(commit=False) # this bc it's a ModelForm, not just Form; don't commit since post field that is FK is being excluded in model, have to add back
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug])) # this will create a get request
        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by("-id"),
            'saved_for_later': self.is_stored_post(request, post.id),
        }
        return render(request, 'blog/post-detail.html', context)

    # # dont need this below anymore since get/post requests above for view include it
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_tags'] = self.object.tags.all() # to get access to a single post's fields
    #     context['comment_form'] = CommentForm() # to create instance of a form based on comment model that you can then access within the template
    #     return context

# # include the post detail including its content
# class SinglePostView(DetailView): # this Detail view auto raises error if object not found and takes a slug as a field
#     template_name = 'blog/post-detail.html'
#     model = Post # this will be the name but in lowercase that you can access in the template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_tags'] = self.object.tags.all() # to get access to a single post's fields
#         context['comment_form'] = CommentForm() # to create instance of a form based on comment model that you can then access within the template
#         return context

# include the post detail including its content
def post_detail(request, slug):
    # identified_post = Post.objects.get(slug=slug)
    identified_post = get_object_or_404(Post, slug=slug) # get_404 gets an object, then with condition specified
    return render(request, 'blog/post-detail.html', {
        'post': identified_post,
        'post_tags': identified_post.tags.all() # now this is a query list, need this in order to get relationships for models
    })


class ReadLaterView(View):
    def get(self, request):
        # get the stored posts / read later
        stored_posts = request.session.get("stored_posts") 

        context = {}

        if stored_posts == None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False 
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts 
            context['has_posts'] = True 

        return render(request, 'blog/stored-posts.html', context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts") 

        # if stored_posts is None, create empty list
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id) # from input form in template
        else:
            stored_posts.remove(post_id)
            
        request.session['stored_posts'] = stored_posts # need to add to session the stored posts

        return HttpResponseRedirect('/')