from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.
def index(request) :
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts' : posts})

def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog.html', {'post':post})