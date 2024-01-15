from django.contrib import admin

from .models import Post, Author, Tag, Comment
# Register your models here.

# config how the admin site looks
class PostAdmin(admin.ModelAdmin): # use ModelAdmin to make changes
    list_filter = ('author', 'tags', 'date',) # add tuples to create filters for views
    list_display = ('title', 'date', 'author',) # this to add columns
    prepopulated_fields = {'slug': ('title',)} # to prepopulate the slug field

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post')

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)