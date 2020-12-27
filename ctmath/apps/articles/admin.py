from django import forms
from django.contrib import admin
from .models import Article, Comment,  Client, Tag
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'text')
    list_filter = ('active', 'create_at')
    search_fields = ('author', 'text')
    actions = ['reject_comments']

    def reject_comments(self, request, queryset):
        queryset.update(active=False)

class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label="Тэкст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Client)

