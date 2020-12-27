from . import views
from .models import Article, Comment, LikeDislike
from django.urls import path

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='articles_list'),
    path('tags/', views.tags_list, name='tags_list'),
    path('create/', views.ArticleCreate.as_view(), name='article_create_url'),
    path('<int:id>/<str:slug>/', views.ArticleDetail.as_view(), name='article_detail_url'),
    path('<int:id>/<str:slug>/update/', views.ArticleUpdate.as_view(), name='article_update_url'),
    path('<int:id>/<str:slug>/delete/', views.ArticleDelete.as_view(), name='article_delete_url'),
    path('<int:id>/<str:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:id>/<str:slug>/addlikes/', views.add_like, name='add_like'),

    path('<int:id>/<str:slug>/like/', views.VotesView.as_view(model=Article, vote_type=LikeDislike.LIKE)),
    path('<int:id>/<str:slug>/dislike/', views.VotesView.as_view(model=Article, vote_type=LikeDislike.DISLIKE)),
    path('comment/<int:id>/like/', views.VotesView.as_view(model=Comment, vote_type=LikeDislike.Like)),
    path('comment/<int:id>/dislike/', views.VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),

    path('tag/create/', views.TagCreate.as_view(), name='tag_create_url'),
    path('tag/<int:id>/<str:slug>/', views.TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<int:id>/<str:slug>/update/', views.TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<int:id>/<str:slug>/delete/', views.TagDelete.as_view(), name='tag_delete_url'),
    path('try-form/', views.my_form, name='my_form'),
    path('acc-form/', views.acc_form, name='account'),
    path('all/', views.ArticleView.as_view()),
    path('up/<int:pk>', views.ArticleView.as_view())
]