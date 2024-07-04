from django import forms
from home.models import Post

class AddPostForm(forms.ModelForm):
    
    class Meta :
        model = Post
        fields = ('image' , 'caption')

class EditPostForm(forms.ModelForm):
    
    class Meta:
        mdoel = Post
        fileds = ('caption',)
