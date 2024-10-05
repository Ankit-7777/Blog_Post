from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment, validate_video_duration

# Post Create View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'video', 'tags']
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags').split(',')

        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if image and video:
            return render(request, self.template_name, {
                'form': self.get_form(),
                'error': 'Please upload either an image or a video, not both.'
            })

        post = Post(title=title, content=content, author=request.user)
        post.save()

        if image:
            post.image = image
        elif video:
            post.video = video
            validate_video_duration(post.video)

        post.save()
        post.tags.add(*tags)
        return redirect(self.success_url)


# Post Update View
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'video', 'tags']
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.tags.clear()  # Clear existing tags
        post.tags.add(*request.POST.get('tags').split(','))  # Add new tags

        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if image and video:
            return render(request, self.template_name, {
                'form': self.get_form(),
                'post': post,
                'error': 'Please upload either an image or a video, not both.'
            })

        if image:
            post.image = image
        elif video:
            post.video = video
            validate_video_duration(post.video)

        post.save()
        return redirect(self.success_url)


# User Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Post List View
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Post.tags.most_common()
        return context


# Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


# Search Functionality
def post_search(request):
    query = request.GET.get('query', '')
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        results = Post.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})


# User Profile View
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# Add Comment to Post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('post_detail', pk=pk)


# Like or Unlike Comment
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk  # Get related post ID for redirect
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post_detail', pk=post_pk)


# Share Post via Email
def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        email = request.POST.get('email')
        send_mail(
            f"Check out this post: {post.title}",
            f"Read {post.title} at {request.build_absolute_uri(post.get_absolute_url())}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('post_detail', pk=pk)
    return render(request, 'share_post.html', {'post': post})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# Post Delete View with Permissions
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
