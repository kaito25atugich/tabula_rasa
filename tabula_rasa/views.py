import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .forms import CommentForm
from .forms import CreateCateForm
from .forms import CreatePostForm
from .forms import SearchForm
from .forms import PostModel
from .forms import IntroductionForm
from .models import Category
from .models import Comment
from .models import Introduction
from .models import Post

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


class ForestBlog(TemplateView):
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        posts = Post.objects.filter(is_public=True).order_by('-created_at')
        recent_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
        categories = Category.objects.filter(post__is_public=True).annotate(Count('kind'))
        introduction = Introduction.objects.get(in_id=1)
        page_obj = paginate_queryset(self.request, posts, 10)
        s_form = SearchForm
        ctx['posts'] = page_obj.object_list
        ctx['recent_posts'] = recent_posts
        ctx['categories'] = categories
        ctx['page_obj'] = page_obj
        ctx['s_form'] = s_form
        ctx['introduction'] = introduction
        return ctx


def page_pre(request, pk):
    post = Post.objects.get(id=pk)
    pre_post = Post.objects.filter(
                is_public=True, created_at__lt=post.created_at
               ).order_by('-created_at')
    return redirect('tabula_rasa:page', pre_post.first().id)

def page_nex(request, pk):
    post = Post.objects.get(id=pk)
    nex_post = Post.objects.filter(
                is_public=True, created_at__gt=post.created_at
               ).order_by('-created_at')
    return redirect('tabula_rasa:page', nex_post.last().id)


class Page(TemplateView):
    template_name = 'blog/page.html'

    def get_context_data(self, pk,**kwargs):
        ctx = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=pk)
        posts = Post.objects.filter(is_public=True).order_by('-created_at')
        prev_post = Post.objects.filter(
                    is_public=True, created_at__lt=post.created_at
                   ).order_by('-created_at')
        next_post = Post.objects.filter(
                    is_public=True, created_at__gt=post.created_at
                   ).order_by('-created_at')
        if next_post:
            nex_post = get_object_or_404(Post, id=next_post.last().id)
            ctx['nex_post'] = nex_post
        if prev_post:
            pre_post = get_object_or_404(Post, id=prev_post.first().id)
            ctx['pre_post'] = pre_post

        recent_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
        categories = Category.objects.filter(post__is_public=True).annotate(Count('kind'))
        comment = Comment.objects.filter(post__id=pk).order_by('-created_at')
        reply = Comment.objects.all()
        introduction = Introduction.objects.get(in_id=1)
        c_form = CommentForm
        s_form = SearchForm
        ctx['post'] = post
        ctx['posts'] = posts
        ctx['comment'] = comment
        ctx['reply'] = reply
        ctx['recent_posts'] = recent_posts
        ctx['categories'] = categories
        ctx['c_form'] = c_form
        ctx['s_form'] = s_form
        ctx['introduction'] = introduction
        return ctx


class CategoryPage(TemplateView):
    template_name = 'blog/category.html'
    def get_context_data(self, pk,**kwargs):
        ctx = super().get_context_data(**kwargs)
        posts = Post.objects.filter(is_public=True).order_by('-created_at').select_related('category')
        category = Category.objects.get(id=pk)
        cats = category.post_set.filter(is_public=True)
        recent_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
        page_obj = paginate_queryset(self.request, cats, 10)
        categories = Category.objects.filter(post__is_public=True).annotate(Count('kind'))
        introduction = Introduction.objects.get_or_create(in_id=1)
        s_form = SearchForm
        ctx['post'] = page_obj.object_list
        ctx['posts'] = posts
        ctx['recent_posts'] = recent_posts
        ctx['category'] = category
        ctx['categories'] = categories
        ctx['page_obj'] = page_obj
        ctx['s_form'] = s_form
        ctx['cats'] = cats
        ctx['introduction'] = introduction
        return ctx


class Edit(TemplateView):
    template_name = 'blog/edit.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pub_posts = Post.objects.filter(is_public=True)
        not_pub_posts = Post.objects.filter(is_public=False)
        introduction = Introduction.objects.get(in_id=1)
        categories = Category.objects.all()

        ctx['pub_posts'] = pub_posts
        ctx['not_pub_posts'] = not_pub_posts
        ctx['introduction'] = introduction
        ctx['categories'] = categories
        return ctx


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Introduction
    template_name = 'blog/update_profile.html'
    form_class = IntroductionForm
    success_url = '/edit/'


class DeleteCategory(LoginRequiredMixin, DeleteView):
    """カテゴリーの削除"""
    model = Category
    template_name = 'blog/delete_category.html'
    success_url = reverse_lazy('tabula_rasa:edit')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, '削除しました')
        return result


class CreateCategory(LoginRequiredMixin, CreateView):
    """カテゴリーの追加"""
    model = Category
    template_name = 'blog/create_category.html'
    form_class = CreateCateForm
    success_url = reverse_lazy('tabula_rasa:edit')
    


class CreatePost(CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('tabula_rasa:edit')
    def form_valid(self, form):
        self.post = form.save(commit=False)
        self.post.created_at = datetime.datetime.now()
        self.post = form.save(commit=True)
        return redirect('tabula_rasa:edit')


class UpdatePost(UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('tabula_rasa:edit')
    def form_valid(self, form):
        """もし公開済みのものを編集した場合には更新日時を更新し、そうでない場合には作成日を更新する"""
        self.post = form.save(commit=False)
        if self.post.is_public:
            update = True
        else:
            update = False
        if update:
            self.post.update_at = datetime.datetime.now()
        else:
            self.post.created_at = datetime.datetime.now()
        self.post = form.save(commit=True)
        return redirect('tabula_rasa:edit')

def make_comment(request, pk):
    c_form = CommentForm(request.POST)
    if c_form.is_valid():
        comment = c_form.save(commit=False)
        comment.post = Post.objects.get(id=pk)
        comment.created_at = datetime.datetime.now()
        comment.save()
        return redirect('tabula_rasa:page', pk)


def make_reply(request, pk, ppk):
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            comment = c_form.save(commit=False)
            comment.reply_to_me = Comment.objects.get(id=pk)
            comment.created_at = datetime.datetime.now()
            comment.save()
            return redirect('tabula_rasa:page', ppk)
    else:
        c_form = CommentForm()
        comment = Comment.objects.get(id=pk)
        introduction = Introduction.objects.get(in_id=1)
        recent_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
        categories = Category.objects.filter(post__is_public=True).annotate(Count('kind'))
        s_form = SearchForm
        context = {
            'c_form': c_form,
            'pk': pk,
            'ppk': ppk,
            'comment': comment,
            'recent_posts': recent_posts,
            'categories': categories,
            's_form': s_form,
            'introduction': introduction,
        }
        return render(request, 'blog/make_reply.html', context)


def search_result(request):
    if request.method == "POST":
        s_form = SearchForm(request.POST)
        if s_form.is_valid():
            text = request.POST['text']
            recent_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:5]
            categories = Category.objects.filter(post__is_public=True).annotate(Count('kind'))
            post_reslt = Post.objects.filter(post__icontains=text)
            page_obj = paginate_queryset(request, post_reslt, 10)
            introduction = Introduction.objects.get(in_id=1)
            context = {
                'text': text,
                'post_reslt': post_reslt,
                'recent_posts': recent_posts,
                'categories': categories,
                's_form': s_form,
                'page_obj': page_obj,
                'introduction': introduction,
            }
            return render(request, 'blog/search_result.html', context)
    return redirect('tabula_rasa:forest_blog')
