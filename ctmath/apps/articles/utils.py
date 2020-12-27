from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View

from .models import Article, Tag


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, {self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        return render(request, self.template, {"form": form})

    def post(self, request):
        submitted_form = self.model_form(request.POST)
        if submitted_form.is_valid():
            new_obj = submitted_form.save()
            return redirect(new_obj)
        return render(request, self.template, {"form": submitted_form})


class ObjectUpdateMixin(View):
    model = None
    model_form = None
    template = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        submitted_form = self.model_form(instance=obj)
        return render(request, self.template, {"form": submitted_form, self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        submitted_form = self.model_form(request.POST, instance=obj)
        if submitted_form.is_valid():
            new_obj = submitted_form.save()
            return redirect(new_obj)
        return render(request, self.template, {"form": submitted_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin(View):
    model = None
    template = None
    url = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        return redirect(request, self.template, {self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        obj.delete()
        return redirect(reverse(self.url))
    