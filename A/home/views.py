from typing import Any
from django.http import HttpRequest
from django.shortcuts import render , get_object_or_404,redirect
from django.views import View
from home.models import Post,Vote,SaveMessage,UserMessage,Relations,UserRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from home.forms import AddPostForm,EditPostForm
from django.contrib import messages
from accounts.models import User
from django.utils.text import slugify
from utils import user_like

# Create your views here.


class HomeView(LoginRequiredMixin,View):
    def get(self,request):
        posts =Post.objects.all()
        can_like = None
        if request.user.is_authenticated :
            can_like =user_like(request.user)
        return render(request , 'home/index.html',{'posts':posts,'can_like':can_like})

    
class UserAddPost(LoginRequiredMixin,View) :
    form_class = AddPostForm
    def get(self,request):
        form = self.form_class
        return render(request , 'home/addpost.html',{'form':form})
    
    
    def post(self,request):
        form =self.form_class(request.POST,request.FILES)
        user = get_object_or_404(User,pk=request.user.id)
        if form.is_valid():
            cd = form.cleaned_data
            Post.objects.create(user=user, image=request.FILES['image'],caption=cd['caption'],slug=slugify(cd['caption'][:30]))
            messages.success(request , 'new post uploaded', 'success')
            return redirect('home:home')
        return render(request , 'home/addpost.html',{'form':form})
    
    
class PostDetailView(LoginRequiredMixin,View):
    def setup(self,request,*args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request,*args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        post=self.post_instance
        can_like =user_like(request.user)
        return render(request,'home/detail.html',{'post':post,'can_like':can_like})

class PostEditView(LoginRequiredMixin,View):
    form_class = EditPostForm
    
    def setup(self,request,*args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request ,*args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request ,'home/efitpost.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data['caption'][:30])
            new_form.save()
            messages.success(request , 'Update post','success')
            return redirect('home:post_detail' , self.post_instance.id)
        
class LikePostView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])
        like = Vote.objects.filter(user=request.user,post=post)
        if like.exists():
            like.delete()
        else :
            Vote.objects.create(user=request.user ,post=post)
        referer = request.META.get('HTTP_REFERER')
        if referer :
            return redirect(referer)
        else :
            return render('home:home')
        
class SaveMessagesView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        print(kwargs['post_id'])
        user_message ,create = UserMessage.objects.get_or_create(user=request.user)
        post = Post.objects.get(pk=kwargs['post_id'])
        save_message = SaveMessage.objects.filter(user_message=user_message,post=post)
        if save_message.exists():
            save_message.delete()
            messages.success(request, 'unsave', 'danger')
        else:
            SaveMessage.objects.create(user_message=user_message, post=post)            
            messages.success(request,'save','success')
        return redirect('home:home')

class SavePostView(LoginRequiredMixin,View):
    def get(self,request):
        user = UserMessage.objects.get(user=request.user.id)
        posts = SaveMessage.objects.filter(user_message=user)
        return render(request,'home/post_save.html',{'posts':posts})
    
    
class UserRelationView(LoginRequiredMixin,View):
    def setup(self, request , *args, **kwargs) :
        self.user_instance = get_object_or_404(User,pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)
    def get(self,request,*args, **kwargs):
        user = Relations.objects.filter(from_user=request.user.id , to_user=self.user_instance).first()
        if user :
            user.delete()
            messages.success(request,'unfollow','danger')
        else :
            Relations.objects.create(from_user = request.user , to_user =self.user_instance)
            messages.success(request,'follow','success')
        return redirect('accounts:user_profile',kwargs['user_id'])

class UserRequestView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        if user.privet == False:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        user = get_object_or_404(User,pk=kwargs['user_id'])
        re = UserRequest.objects.filter(from_user=request.user,to_user=user)
        if re.exists():
            re.delete()
            messages.success(request,'delete request','danger')
        else:
            UserRequest.objects.create(from_user=request.user,to_user=user)
            messages.success(request,'sent request','success')
        return redirect('accounts:user_profile',kwargs['user_id'])

            
class UserDetailRequestsView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User,pk=kwargs['user_id'])
        if request.user.id != user.id:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        user = get_object_or_404(User,pk=kwargs['user_id'])
        re =UserRequest.objects.filter(to_user = user)
        return render(request,'home/requests.html',{'re':re})

class UserAcceptView(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        user = get_object_or_404(User,pk=request.user.id)
        f_user = get_object_or_404(User,pk=kwargs['user_id'])
        re = UserRequest.objects.filter(from_user=f_user,to_user=user)
        if re.first():
            Relations.objects.create(from_user=f_user,to_user=user)
            re.delete()
        else:
            messages.error(request,'error','danger')
        return redirect('home:requests',user.id)
        