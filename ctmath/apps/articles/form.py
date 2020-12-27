from django import forms
from PIL import Image
import datetime
from durationwidget.widgets import TimeDurationWidget
from .models import *
from django.core.exceptions import ValidationError


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'description', 'poster', 'text', 'author', 'tags', 'slug', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'size': '5'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'special'})
        }


   # title = forms.CharField(label='Назва артыкула', max_length=96,
  #                                  error_messages={'required': 'Калі ласка, прыдумайце назву артыкула'})
 #   description = forms.CharField(label='Апісанне', max_length=256)
#    new_period = forms.DurationField(required=False, initial=datetime.timedelta(days=7))
 #   image = forms.ImageField(required=False, help_text='в формате .jpg')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




class AccountForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=16)
    birthday = forms.DateField(widget=forms.SelectDateWidget)
    sex = forms.ChoiceField(choices=[("1", "М"), ("2", "Ж")])
    work_experience = forms.DurationField(widget=TimeDurationWidget)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == "create":
            raise ValidationError('Slug do not CREATE')
        if Tag.objects.filter(slug__ixact=new_slug).count():
            raise ValidationError('Not unique')
        return new_slug

