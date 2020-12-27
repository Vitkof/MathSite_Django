from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_data),
    path('filter/', views.FilterView.as_view()),
    path('orderby/', views.OrderByView.as_view()),
    path('all/', views.AllView.as_view()),
    path('none/', views.NoneView.as_view()),
    path('values/', views.ValuesView.as_view()),
]
