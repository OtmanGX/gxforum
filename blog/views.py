from django.views.generic import ListView, DetailView

from .models import Post


class PostsListView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"


class PostDetailView(DetailView):
    template_name = "blog/post.html"
    model = Post
    context_object_name = "post"
    slug_url_kwarg = "slug"
