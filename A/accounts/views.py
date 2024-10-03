from django.core.signals import request_started
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import User
from .forms import UserRegistertionForm,UserLoginForm,UserEditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post,Relations,UserRequest
# Create your views here.



class UserRegisterView(View):
    form_class = UserRegistertionForm
    template_name = 'accounts/register.html'
    
    def get(self,request):
        form = self.form_class
        return render(request , self.template_name ,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if request.FILES.get('profile') == None:
                User.objects.create_user(username=cd['username'],full_name=cd['full_name'],email=cd['email'],birthday=cd['birthday'],password=cd['password1'])
            else :
                User.objects.create_user(profile=request.FILES['profile'],username=cd['username'],full_name=cd['full_name'],email=cd['email'],birthday=cd['birthday'],password=cd['password1'])
            messages.success(request ,'register','success')
            return redirect('home:home')
        messages.error(request,'form is wrong','danger')
        return render(request , self.template_name ,{'form':form})
        
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def get(self,request):
        form = self.form_class
        return render(request , self.template_name,{'form':form})
    
    def post(self,request):
        form =self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data        
            user = authenticate(request , username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'login','success')
                return redirect('home:home')
            messages.error(request,'username or password is wrong','danger')
        return render(request,self.template_name,{'form':form})

class UserLogoutView(LoginRequiredMixin,View):
    
    def get(self,request):
        logout(request)
        messages.success(request,'success','success')
        return redirect('home:home')
    
class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User , pk=user_id)
        follow = Relations.objects.filter(from_user = request.user.id,to_user=user)
        print('-'*99)
        followers = Relations.objects.filter(to_user=user_id)
        following = Relations.objects.filter(from_user=user_id)
        posts = Post.objects.filter(user=user_id)
        re = UserRequest.objects.filter(from_user = request.user.id,to_user=user)
        is_request =False
        if re.exists():
            is_request=True
        is_follow = False
        if follow.exists():
            is_follow=True
        context = {'user':user,
                        'posts':posts,
                        'is_follow':is_follow,
                        'followers':followers,
                        'following':following,
                        'is_request':is_request}
        print(context)
        return render(request , 'accounts/profile.html',context)
    
class UserEditeProfileView(LoginRequiredMixin,View):
    form_class = UserEditProfileForm
    
    def get(self,request):
        form = self.form_class(instance=request.user)
        self.image = request.user.profile
        return render(request , 'accounts/editprofile.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            if request.FILES.get('profile') != None:
                user=User.objects.get(pk=request.user.id)
                user.profile.delete()
                print('-'*99)
            form.save()
            messages.success(request,'edit success','success')
            return redirect('accounts:user_profile',request.user.id)
        messages.error(request , 'warning','warning')
        return render(request , 'accounts/editprofile.html',{'form':form})
