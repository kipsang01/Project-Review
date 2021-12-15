from django.shortcuts import render, redirect,get_object_or_404
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import PostSerializer,ProfileSerializer

from .forms import RegisterUserForm,PostForm,RatingForm, ProfileForm
from .models import Post,Rating,Profile

# Create your views here.
def home(request):
    posts = Post.get_posts()

    
    return render(request, 'home.html',{'posts':posts})

# Adding post
@login_required(login_url='/accounts/login')
def post_image(request):
    if request.method == 'POST':
        current_user = request.user
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = current_user
            post.save()
            messages.success(request,('Project Posted!'))
        return HttpResponseRedirect(request.path_info)
           
    else:
        form = PostForm()
        
    return render(request,'add_post.html', {'form':form})

#one post
@login_required(login_url='/accounts/login')
def post(request,post_id):
    current_user = request.user
    post = get_object_or_404(Post,id=post_id)
    print(post)
    print(current_user)
    ratings = Rating.objects.all()
    rated = Rating.objects.filter(post = post,author= current_user).first()
    print(rated)
    if request.method == 'POST':
        if rated is None:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating =form.save(commit=False)
                rating.post = post
                rating.author = current_user
                rating.save()
                print(rating)
                messages.success(request,('Rated successfully'))
               
            else:
                messages.error(request,('Something Went Wrong'))
            return redirect('post',post_id=post.id)
        else:
            messages.error(request,('Already rated'))
            return redirect('post',post_id=post.id)
    else:
        form = RatingForm()
        
    return render(request,'post.html', {'post':post,'form':form,'ratings':ratings,'rated':rated})


# Page for profile
def user_profile(request,username):
    user = User.objects.filter(username=username).first()
    if user == request.user:
        return redirect('my_profile')
    profile = Profile.objects.filter(user=user).first()
    posts = Post.objects.filter(author=user)
    return render(request, 'userprofile.html', {'profile':profile,'posts':posts})


#logged in user profile
@login_required(login_url='/accounts/login')
def my_profile(request):
    user = request.user
    user = User.objects.filter(username=user.username).first()
    posts = Post.objects.filter(author=user)
    return render(request, 'profile.html', {'user': user,'posts':posts})


# search posts by titles
def search_post(request):
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        posts = Post.search_post(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{'posts':posts})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

# Edit profile
@login_required(login_url='/accounts/login')
def edit_profile(request):
    user = request.user
    user = User.objects.filter(username=user.username).first()
    profile = get_object_or_404(Profile,user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profileform = form.save(commit=False)
            profileform.user = user
            profileform.save()
            messages.success(request,('Update saved'))
        return redirect('my_profile')
           
    else:
        form = ProfileForm()
    
    return render(request, 'edit_profile.html', {'form':form, 'user': user})


    
# Register user
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(username = username,password=password)
            login(request,user)
            messages.success(request,('Registration successfull and logged in'))
            return redirect('home')
           
    else:
        form = RegisterUserForm()
        
    return render(request,'registration/registration_form.html', {'form':form})


#Api endpoints

class PostsList(APIView):
    def get(self, request, format=None):
        all_posts = Post.objects.all()
        serializers = PostSerializer(all_posts, many=True)
        return Response(serializers.data)
    
class UserProfiles(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializers = ProfileSerializer(profiles, many=True)
        return Response(serializers.data)