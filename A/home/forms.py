from django import forms
from .models import Post

class AddPostForm(forms.ModelForm):
    
    class Meta :
        model = Post
        fields = ('image' , 'caption')

        def __init__(self,*args,**kwargs):
            super(AddPostForm, self).__init__(*args, **kwargs)
            self.fields['image'].widget.attrs.update({'class': 'form-control'})
            self.fields['caption'].widget.attrs.update({'class': 'form-control'})

class EditPostForm(forms.ModelForm):
    
    class Meta:
        mdoel = Post
        fileds = ('caption',)
