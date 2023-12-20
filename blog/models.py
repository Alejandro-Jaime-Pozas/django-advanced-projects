from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.



class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField() # takes care of validating that email is correct format

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.caption

        
class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True) # updates the date each time the object is saved, not a create date
    slug = models.SlugField(unique=True, ) # slug fields auto add db_index=True
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, null=True, related_name='posts')

    def __str__(self) -> str:
        return f"{self.title} | by: {self.author}"