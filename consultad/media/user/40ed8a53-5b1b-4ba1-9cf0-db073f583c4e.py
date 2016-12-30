from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from .models import Blog
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

@csrf_protect


def index(request):
    blogs = Blog.objects.all()
    return render(request, 'login/blog.html', {'blog_list': blogs})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render_to_response(
        'registration/login.html', {'user': request.user}

    )
def detail(request):
    blogs = Blog.objects.all()
    return render(request, 'login/blogs.html', {'blog_list': blogs})


def add_blog(request ):

    if request.method == 'POST' :
             blog = request.POST.get('blog')
             username= request.user
             form = Blog(blog=blog, username= request.user)
             form.save()
             blog_list = Blog.objects.all()
             context = {'form': form, 'blog_list': blog_list }
             return render(request, 'login/blogs.html', context)
    else:
        form = Blog()
        return render(request, 'login /blogs.html')

def edit_blog(request, blog_id, blog_user, user):
    if request.method == 'POST':
        if blog_user == user:
                 blog = Blog.objects.get(pk=blog_id)
                 blog.blog = request.POST.get('blog')
                 blog.save()
                 blog_list = Blog.objects.all()
                 context = { 'blog_list': blog_list}

                 return render(request, 'login/blogs.html', context)

        else:
                 return HttpResponse("you cannot edit this blog")

    else:
        form = Blog()
        return render(request, 'login /blogs.html')

def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'login/view.html', {'blog': blog})


'''def edit_blog(request):
    if request.method  == 'POST':
        if(request.user == blog.user)'''
