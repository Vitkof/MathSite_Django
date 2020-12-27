from django.db import models
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from model_utils import Choices
import os
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse
from time import time
from PIL import Image


def gen_slug(st):
    new_slug = slugify(st, allow_unicode=True)
    return new_slug

#def pre_save_receiver(sender, instance, *args, **kwargs):
#    if not instance.slug:
#        instance.slug = unique_slug_generator(instance)
#pre_save.connect(pre_save_receiver, sender=Article)

class Author(models.Model):
    name = models.CharField("iмя", max_length=32)
    age = models.PositiveSmallIntegerField("ўзрост", default=0)
    info = models.CharField("інфармацыя", max_length=384, blank=True, default='')
    image = models.ImageField("фота", upload_to="authors/")
    accession_date = models.DateField("працягласць", default=date.today)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Аўтар"
        verbose_name_plural = "Аўтары"


class Tag(models.Model):
    title = models.CharField(max_length=32, help_text="1 слова")  # 1 word
    slug = models.SlugField(default='')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэгі'


class Article(models.Model):
    STATUSES = Choices(
        (0, 'draft', _('draft')),
        (1, 'published', _('published')))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="аўтар", null=True)
    title = models.CharField("назва", max_length=96, unique=True)
    description = models.CharField("апісанне", max_length=256, blank=True, default='')
    text = RichTextUploadingField("тэкст", blank=True, default='', db_index=True)
    pub_date = models.DateTimeField("дата публікацыі", null=True)
    updated = models.DateTimeField("дата абнаўлення", auto_now=True)
    new_period = models.DurationField(default=timedelta(days=7),
                                      help_text="Выкарыстоўвайце гэта поле, калі вам патрэбна"
                                                "інфармацыя пра час навізны артыкула."
                                                "Па змаўчанні - 7 дзён")
    poster = models.ImageField("постэр артыкула", blank=True, null=True, upload_to='article_poster/%Y/%m/%d')
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=STATUSES.draft)
    slug = models.SlugField(max_length=128, unique=True, allow_unicode=True,
                            help_text="URL-slug мае важнае значэнне для індэксацыі."
                                      "1. Вызначце найбольш важныя ключавыя словы ў вашым артыкуле(дап: keywordtool.io)"
                                      "2. Зламаць усе непатрэбныя словы, любыя 'стопы': 'гэты','i','з','г.д.(тд.)'."
                                      "3. Стварайце ваш slug як мага карацей. 4 ці 5 слоў з'яўляецца стандартам."
                                      "4. Сціснуць яго, але ваш slug павінен, каб меў нейкі сэнс наогул")
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    likes = models.PositiveSmallIntegerField(default=0)
    # класс GenericRelation не создает дополнительных миграций базы данных
    votes = GenericRelation('LikeDislike', related_query_name='articles')  # модел в кавычках

   # def get_absolute_url(self):
   #     return reverse('article_detail_url', kwargs={'id': self.id})

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - timedelta(days=7))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date', 'title']
        verbose_name = 'Артыкул'
        verbose_name_plural = 'Артыкулы'


class ArticleImages(models.Model):
    """Малюнкі з артыкула"""
    title = models.CharField("Загаловак", max_length=100)
    image = models.ImageField("Малюнак", upload_to="article_images/")
    article = models.ForeignKey(Article, verbose_name="Артыкул", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Малюнак'
        verbose_name_plural = 'Малюнкi'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField("аўтар", max_length=32)
    text = models.CharField("тэкст каментара", max_length=256)
    create_at = models.DateTimeField(verbose_name="створаны ў", auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    parent = models.ForeignKey('self', verbose_name="бацька", on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    # класс GenericRelation не создает дополнительных миграций базы данных
    votes = GenericRelation('LikeDislike', related_query_name='comments')

    def __str__(self):
        return f"{self.author} - {self.article}"

    class Meta:
        ordering = ('-rating', '-create_at')
        verbose_name = 'Каментар'
        verbose_name_plural = 'Каментары'


class LikeDislikeManager(models.Manager):
    def likes(self):
        return self.get_queryset().filter(vote__gt=0)
    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)
    # Забираем суммарный рейтинг
    def sum_rating(self):
        return self.get_queryset().aggregate(models.Sum('vote')).get('vote__sum') or 0
    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__create_at')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (LIKE, 'падабаецца'),
        (DISLIKE, 'не падабаецца')
    )
    vote = models.SmallIntegerField(verbose_name=_("Голас"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=_("Карыстальнік"))
    # тип контента (Статьи, Комменты...)
    # ID первичного ключа экземпляра модели, для которой создаётся связь
    # поле для связи с любой моделью
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.SmallIntegerField()
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()





class CustomQuerySet(models.query.QuerySet):
    def with_comments_counter(self):
        return self.annotate(comm_count=models.Count('comment_set'))


def get_upload_path(instance, filename):
    return os.path.join('account/avatars/', datetime.now().date().strftime("%Y/%m/%d"), filename)


class Client(models.Model):
    avatar = models.ImageField(blank=True, upload_to=get_upload_path)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    second_email = models.EmailField("эл.пошта")
    name = models.CharField(max_length=64)
    invoice = models.FileField()
    discount_size = models.DecimalField(max_digits=5, decimal_places=2)
    user_uuid = models.UUIDField(editable=False)
    client_ip = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")


