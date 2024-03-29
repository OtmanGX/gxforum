from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from utils.deco import *
from .models import Board, Post, Topic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NewTopicForm, NewPostForm

PAGE_TOPIC_SIZE = 3
PAGE_BOARD_SIZE = 10


class BoardListView(ListView):
    template_name = "forum/index.html"
    context_object_name = "boards"
    model = Board


class TopicListView(ListView):
    template_name = "forum/board.html"
    model = Topic
    context_object_name = "topics"
    paginate_by = PAGE_BOARD_SIZE

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get("pk"))
        queryset = self.board.topics.order_by("-last_updated").annotate(replies=Count('posts') - 1)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)


class PostsListView(ListView):
    template_name = "forum/topic.html"
    model = Post
    context_object_name = "posts"
    paginate_by = PAGE_TOPIC_SIZE

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk=self.kwargs["topic_id"])
        queryset = self.topic.posts.order_by("created_at")
        return queryset

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True  # <-- until here
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        post = Post()
        topic = get_object_or_404(Topic, pk=self.kwargs["topic_id"])
        if request.POST.get('message'):
            post.message = request.POST['message']
            post.topic = topic
            post.created_by = self.request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
        url = '{url}?page={page}'.format(
            url=reverse('forum:topic', kwargs={'id': topic.board.pk, 'topic_id':topic.pk}),
            page=topic.get_page_count()
        )
        return redirect(url)
        # return HttpResponseRedirect(request.path_info)


class NewPostView(LoginRequiredMixin, CreateView):
    template_name = 'forum/new_topic.html'
    form_class = NewTopicForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, pk=self.kwargs['id'])
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        user = self.request.user
        topic.board = self.get_context_data().get('board')
        topic.created_by = user
        topic.save()
        Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=user)
        return redirect('forum:board', pk=topic.board.pk)


@user_owner_required
class EditPostView(LoginRequiredMixin, UpdateView):
    success_message = "The post has been successfully updated"
    template_name = "forum/new_topic.html"
    model = Post
    fields = ('message',)
    pk_url_kwarg = 'post_uk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.get_object().topic.board
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        messages.success(self.request, self.success_message)
        return redirect('forum:topic', id=post.topic.board.pk, topic_id=post.topic.pk)


@user_owner_required
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'pk'
    success_message = "The post has been successfully deleted"

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("forum:topic", args=[self.get_object().topic.board.pk, self.get_object().topic.pk])


@user_owner_required
class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    pk_url_kwarg = 'pk'
    success_message = "The topic has been successfully deleted"

    def delete(self, request, *args, **kwargs):
        self.board_pk = self.get_object().board.pk
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("forum:board", args=[self.board_pk])

    # def delete(self, request, *args, **kwargs):
    #     messages.success(self.request, "The post has been successfully deleted")
    #     super(self, request, *args, **kwargs).delete()
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
