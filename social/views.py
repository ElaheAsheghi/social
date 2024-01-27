from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.mail import send_mail
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import views
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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
    paginator = Paginator(posts,2)
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


#Post Detail
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:2]
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post':post,
        'similar_post':similar_post,
        'comments':comments,
        'form':form,
    }
    return render(request, "social/detail.html", context)


#Search
def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = Post.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(similarity__gt=0.1)
            results2 = Post.objects.annotate(similarity=TrigramSimilarity('tags__name', query)).filter(similarity__gt=0.1)
            results = (results1 | results2).order_by('similarity')
        context = {
            'query':query,
            'results':results,
        }
        print(type(Post.tags))
        print(type(Post.description))
        print(type(Post.tagged_items))

        return render(request, 'social/search.html', context)
    

#Comment
# @login_required(next='blog:post_detail')
@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
    else:
        form = CommentForm()
    comments = post.comments.all()
    context = {
        'post':post,
        'form':form,
        'comments':comments,
    }
    return render(request, "forms/comment.html", context)