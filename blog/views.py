from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CreateUserForm, BlogForm
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve Post By Id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    # Form was submitted
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        # Form fields passed the validation
        if form.is_valid():
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n \n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message,
                      'prasannasomoshi@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request, 'Account succesfully created for ' + user)
            return redirect('blog:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/blog')
        else:
            messages.info(request, "Username or Password is incorrect!")

    context = {}
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('blog:login')


def writeblog(request):
    form = BlogForm()
    if request.method == "POST":

        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blog:post_list")

    return render(request, "blogform.html", {'form': form})
