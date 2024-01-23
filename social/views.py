from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.mail import send_mail
from django.contrib.auth import views
from .forms import *
from .models import *


# Create your views here.
#profile
def profile(reguest):
    return HttpResponse("پروفایل")


#Login
class UserLoginView(views.LoginView):
    form_class = LoginForm


#Logout
def Logout(request):
    return HttpResponse("خارج شدید!")


#Register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})


#UserEdit
@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form':user_form,
    }
    return render(request, 'registration/edit_user.html', context)
    

#Ticket
def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'], message,\
                       'socialwebproject2024@gmail.com', ['asheghielahe@gmail.com'], fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form':form, 'sent':sent})


#Post List
def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    #Paginator
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = Paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts':posts,
        'tag':tag,
    }
    return render(request, "social/list.html", context)


#Create Post
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form':form})