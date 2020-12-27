from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
# from django.views.generic import View
from django.views import View
from django.contrib.contenttypes.models import ContentType
from .models import Article, Tag, Comment, Client, LikeDislike
from .form import ArticleForm, AccountForm, TagForm
from .utils import *
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from uuid import uuid4
from pathlib import Path

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .serializers import ArticleSerializer


class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({'articles': serializer.data})

    def post(self, request):
        new_art = request.data.get('article')
        serializer = ArticleSerializer(data=new_art)
        if serializer.is_valid(raise_exception=True):
            art_saved = serializer.save()
        return Response({"success": f"Артыкул '{art_saved.title}' створаны паспяхова"})

    def put(self, request, pk):
        extra = get_object_or_404(Article.objects.all(), pk=pk)
        up_art = request.data.get('article')
        serializer = ArticleSerializer(instance=extra, data=up_art, partial=True)
        if serializer.is_valid(raise_exception=True):
            art_saved = serializer.save()
        return Response({"success": f"Артыкул '{art_saved.title}' паспяхова абноўлены"})

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.get(pk=pk))
        article.delete()
        return Response({"message": f"Артыкул '{article.title}' быў выдалены."}, status=204)


class ArticleDetail(View):
    def get(self, request, id):
        article = get_object_or_404(Article, id=id)
        latest_comments = article.comment_set.order_by('-id')[:7]
        return render(request, 'articles/article_detail.html',
                      {'article': article, 'latest_comments': latest_comments})


class ArticleCreate(ObjectCreateMixin, View):
    model_form = ArticleForm
    template = 'articles/article_create.html'


class ArticleUpdate(ObjectUpdateMixin, View):
    model = Article
    model_form = ArticleForm
    template = 'articles/article_update.html'


class ArticleDelete(ObjectDeleteMixin, View):
    model = Article
    template = 'articles/article_delete.html'
    url = 'articles_list'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'articles/tag_detail.html'


class TagCreate(ObjectCreateMixin, View):
    model_form = TagForm
    template = 'articles/tag_create.html'


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'articles/tag_update.html'


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    template = 'articles/tag_delete.html'
    url = 'tags_list'


def index(request):
    latest_articles = Article.objects.order_by('-pub_date')
    return render(request, 'articles/list_articles.html', {'latest_articles': latest_articles})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'articles/list_tags.html', {"tags": tags})


def add_comment(request, slug):
    try:
        a = Article.objects.get(slug__iexact=slug)
    except:
        raise Http404("Артыкул не знойдзены!")
    if request.method == "POST" and ("pause" not in request.session):
        a.comment_set.create(author=request.POST['name'], text=request.POST['text'])
        request.session.set_expiry(60)
        request.session["pause"] = True
    return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))


def add_like(request, id):
    if id in request.COOCKIES:
        return HttpResponseRedirect('/')
    else:
        if "test1" not in request.session:
            article = get_object_or_404(Article, id=id)
            article.likes += 1
            article.save()
            request.session.set_expiry()
            request.session["pause"] = True
            response = HttpResponseRedirect('/')
            response.set_cookie(id, "test1")
            return response
        return HttpResponseRedirect('/')


class VotesView(View):
    model = None
    vote_type = None  # тип голоса Like/Dislike

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                                  object_id=obj.id, user=request.user)

        except:
            pass


def create_client(request):
    with open('Green-card.txt', 'r') as _file:
        tmp_f = _file.read()

    Client.objects.create(**{
        'second_email': 'admin@admin9.ru',
        'name': "MyName",
        'invoice': tmp_f,
        'uuid': uuid4(),
        'discount_size': Decimal("5.05"),
        'client_ip': "192.168.1.55"
    })
    return HttpResponse('Created')


def my_form(request):
    form = ArticleForm(request.GET)
    if form.is_valid():
        print(form.cleaned_data)
        print(form.errors)
    else:
        print(form.cleaned_data)
        print(form.errors)
    return render(request, 'form-page.html', {'form': form})


def acc_form(request):
    form = AccountForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        file_path = Path(settings.MEDIA_ROOT / form.cleaned_data['profile_picture'].name)
        with open(file_path, 'wb+') as file:
            for chunk in form.cleaned_data['profile_picture']:
                file.write(chunk)


    else:
        print(form.errors)

    return render(request, 'form-page.html', {'form': form})
