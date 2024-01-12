from django import forms 

from .models import Comment 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name': 'Your Name',
            'user_email': 'Your Email',
            'text': 'Your Comment'
        } # to override django default names to form fields