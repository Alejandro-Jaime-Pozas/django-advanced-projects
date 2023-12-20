from django.contrib import admin

from .models import Post, Author, Tag
# Register your models here.

# config how the admin site looks
class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'tags', 'date',) # add tuples to create filters for views
    list_display = ('title', 'date', 'author',) # this to add columns
    prepopulated_fields = {'slug': ('title',)} # to prepopulate the slug field

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)