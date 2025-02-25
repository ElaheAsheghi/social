from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
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
from django.contrib import messages


# Create your views here.
#profile
def profile(request):
    user = request.user
    saved_posts = user.saved_posts.all()[:5]
    my_posts = user.user_posts.all()
    context = {
        'user' : user,
        'saved_posts' : saved_posts,
        'my_posts' : my_posts,
    }
    return render(request, 'social/profile.html', context)


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
            user = request.user
            message = f"{user}:\n\n{cd['message']}"
            send_mail(cd['subject'], message,\
                       'socialwebproject2024@gmail.com', ['asheghielahe@gmail.com'], fail_silently=False)
            sent = True
            messages.success(request, 'sent!')
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form':form, 'sent':sent})


#Post List
def post_list(request, tag_slug=None):
    posts = Post.objects.select_related('author').all().order_by('-total_likes')
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
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list_ajax.html', {'posts':posts})
    
    context = {
        'posts':posts,
        'tag':tag,
    }
    return render(request, "social/list.html", context)


#Create Post
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(data=request.POST, files=request.FILES)
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
    comments = post.comments.all()[:5]
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
        return render(request, 'social/search.html', context)
    

#Comment
# @login_required(next='social:post_detail')
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
            UserCommentActivity.objects.get_or_create(user=request.user, post=post)
    else:
        form = CommentForm()
    comments = post.comments.all()
    context = {
        'post':post,
        'form':form,
        'comments':comments,
    }
    return render(request, "social/detail.html", context)


#Login
class UserLoginView(views.LoginView):
    form_class = LoginForm
    

#Logout
def userlogout(request):
    return render(request, "registration/logout.html")

class UserLogoutView(views.LogoutView):
    form_class = LogoutForm


#Edit Post
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    shared = False
    if request.method == 'POST':
        form = CreatePostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect(post)
    else:
        form = CreatePostForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, "forms/edit_post.html", context)


#Delete Post
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, "forms/delete_post.html", {'post': post})
    
def deleted_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('social:post_list')


#Like Post
@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            UsersLikeActivity.objects.filter(user=request.user, post=post).delete()
            liked = False
        else:
            post.likes.add(user)
            UsersLikeActivity.objects.get_or_create(user=request.user, post=post)
            liked = True
        post_likes_count = post.likes.count()
        response_data = {
            'liked': liked,
            'likes_count': post_likes_count,
        }    
    else:
        response_data = {'error': 'Invalid post_id'}
    return JsonResponse(response_data)


#Save Post
@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False
        else:
            post.saved_by.add(user)
            saved = True
        response_data = {
            'saved': saved,
        }    
    else:
        response_data = {'error': 'Invalid post_id'}
    return JsonResponse(response_data)


#User List
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'social/user_list.html', {'users' : users})


#User Detail
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    user_posts = user.user_posts.all()
    return render(request, 'social/user_detail.html', {'user' : user, 'user_posts' : user_posts})


#User Follow
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            following_count = user.following.count()
            followers_count = user.followers.count()
        
            return JsonResponse({'follow':follow, 'following_count':following_count, 'followers_count':followers_count})
        except user.DoesNotExist:
            return JsonResponse({'error' : 'user does not exist'})
    return JsonResponse({'error' : 'invalid request'})


#Admin Messages
def admin_messages(request):
    user = request.user
    messages = user.admin_messages.all()
    return render(request, 'social/admin_messages.html', {'messages' : messages})

#Post Likes
def users_liked_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    users_have_liked = post.likes.all()
    return render(request, 'social/users_liked_post.html', {'users_have_liked' : users_have_liked})


#User Following
def user_following_list(request, username):
    user = get_object_or_404(User, username=username)
    following_list = user.following.all()
    return render(request, 'social/user_following.html', {'following_list' : following_list})


#User Followers
def user_followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers_list = user.followers.all()
    return render(request, 'social/user_followers.html', {'followers_list' : followers_list})


#Users Activity
def users_activities(request):
    activity = UsersLikeActivity.objects.all()
    activity2 = UserCommentActivity.objects.all()
    activity3 = Contact.objects.all()
    return render(request, 'social/activity.html', {'activity' : activity, 'activity2' : activity2, 'activity3' : activity3})


#Following Users Activity
def following_users_activities(request):
    user = request.user
    following = user.following.all()
    activity = UsersLikeActivity.objects.filter(user__in=following)
    activity2 = UserCommentActivity.objects.filter(user__in=following)
    activity3 = Contact.objects.filter(user_from__in=following)
    return render(request, 'social/following_activity.html', {'activity': activity, 'activity2': activity2, 'activity3': activity3,})


#Ajax Comment
@require_POST
def ajax_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            name = request.user
            
            body = request.POST.get('body')
                
            new_cm = Comment(name=name, body=body, post=post)
            new_cm.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return render(request, 'forms/ajax_comment.html', {'new_cm':new_cm})
    return render(request, 'forms/comment.html', {})