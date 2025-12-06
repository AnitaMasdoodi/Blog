from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from .forms import PostForm, CommentForm, PostUpdateForm
from .models import Post, Aboutme, Category, Comment


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()[::-1]
        posts4 = Post.objects.all()[::-1][:4]
        aboutme = Aboutme.objects.all()
        categories = Category.objects.all()
        posts_with_approved_comments = []
        for post in posts:
            approved_comments_count = post.comments.filter(is_approved=True).count()
            post.approved_comments_count = approved_comments_count
            posts_with_approved_comments.append(post)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)  # دریافت صفحه موردنظر
        context = {
            "posts":posts,
            'posts4':posts4,
            'aboutme':aboutme,
            'categories':categories,
        }
        return render(request, 'home/index.html', context)


class CreatePostView(View):
    form_class = PostForm
    temp = 'home/create-post.html'

    def get(self, request):
        return render(request, self.temp, {'form': self.form_class()})    

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            if not new_post.slug:
                new_post.slug = slugify(new_post.title)
            new_post.save()
            messages.success(request, 'Your post has been created.', 'success')
            return redirect(new_post.get_absolute_url())

        messages.error(request, "Error! Something went wrong.", 'warning')
        return render(request, self.temp, {'form': form})


class PostDetailView(View):
    temp = 'home/post-with-right-sidebar.html'
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug):
        posts4 = Post.objects.all()[::-1][:4]
        aboutme = Aboutme.objects.all()
        categories = Category.objects.all()
        self.post_instance = Post.objects.get(slug=slug)
        comments = self.post_instance.comments.filter(is_approved=True)
        context = {
            'post': self.post_instance,
            'form': self.form_class(),
            'posts4':posts4,
            'aboutme':aboutme,
            'categories':categories,
            'comments':comments,
        }
        return render(request, self.temp, context)

    @method_decorator(login_required)
    def post(self, request, slug):
        user = request.user
        if user.is_superuser:
            form = self.form_class(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = self.post_instance
                new_comment.user = user
                new_comment.is_approved = True
                new_comment.save()
                messages.success(request, "Your comment has been posted successfully.")
                return redirect(self.post_instance.get_absolute_url())

        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)
        recent_comments = Comment.objects.filter(user=user, date__gte=one_hour_ago)

        if recent_comments.count() >= 10:
            first_comment_time = recent_comments.earliest('date').date
            ban_time = first_comment_time + timedelta(hours=24)
            
            if now < ban_time:
                messages.error(request, f"You have exceeded the limit of 10 comments in an hour. You can post again after {ban_time.strftime('%Y-%m-%d %H:%M:%S')}.")
                return redirect(self.post_instance.get_absolute_url())
            
        form = self.form_class(request.POST)
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to post a comment.')
            return redirect('login')
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.post_instance
            new_comment.user = request.user
            new_comment.is_approved = False
            new_comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
            return redirect(self.post_instance.get_absolute_url())
        return render(request, self.temp, {'form':form})


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    temp = 'home/post-edit.html'


    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.post_instance.author:
            messages.error(request, "This post is not yours. you can't change it.", 'danger')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        form = self.form_class(instance=self.post_instance)
        return render(request, self.temp, {'form':form})

    def post(self, request, slug):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been successfully updated.', 'success')
            return redirect(self.post_instance.get_absolute_url())
        messages.error(request, 'Error! Something went wrong.', 'warning')
        return render(request, self.temp, {'form':form})


class PostDeleteView(View):
    temp = 'home/delete-post.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.post_instance.author:
            messages.error(request, "This post is not yours. you can't change it.", 'danger')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        return render(request, self.temp, {'post':self.post_instance})

    def post(self, request, slug):
        self.post_instance.delete()
        messages.success(request, 'Your post has been successfully deleted.', 'warning')
        return redirect('home')


class PostSearchView(View):
    temp = 'home/search_results.html'

    def get(self, request):
        query = request.GET.get('q', '')  # مقدار پیش‌فرض خالی باشد
        posts = Post.objects.filter(text__icontains=query) if query else None

        context = {
            'query': query,
            'posts': posts,
        }
        return render(request, self.temp, context)
    

class CategoryPostsView(View):
    temp = 'home/category_posts.html'

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        posts_list = Post.objects.filter(category=category).order_by('-date')
        posts_with_approved_comments = []
        for post in posts_list:
            approved_comments_count = post.comments.filter(is_approved=True).count()
            post.approved_comments_count = approved_comments_count
            posts_with_approved_comments.append(post)

        paginator = Paginator(posts_list, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        context = {
            'category': category,
            'posts': posts
        }
        return render(request, self.temp, context)
    

class ProfileView(View):
    temp = 'home/profile.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user)[::-1]
        context = {'user': user, 'posts': posts}
        return render(request, self.temp, context)
    


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', slug=slug)