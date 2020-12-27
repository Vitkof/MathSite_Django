import csv
from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponse


def upload_data(request):
    with open('universities_scores.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                print('Tyt!!!')
                _, created = UniverModel.objects.get_or_create(
                    location=row[2],
                    overall=row[3],
                    teaching=row[4],
                    research=row[5],
                    citations=row[6],
                    industry_income=row[7],
                    international_outlook=row[8]
                )
                print(_, created)
            except:
                pass
    with open('universities_ranking.csv') as f2:
        reader2 = csv.reader(f2)
        for row2 in reader2:
            try:
                up = UniverModel.objects.get(pk=row2[0])
                up.title = row2[1]
                up.number_students = int(row2[3].replace(',', ''))
                up.students_staff = row2[4]
                up.percent_foreigners = row2[5][:-1]
                up.gender_ratio = row2[6]
                up.save()
            except:
                pass

    return HttpResponse('Done!')


class FilterView(ListView):
    template_name = 'univermodel_list.html'
    queryset = UniverModel.objects.filter(
        ~Q(title__startswith="Bel") | ~Q(title__startswith="Mos"))

class OrderByView(ListView):
    template_name = 'univermodel_list.html'
    queryset = UniverModel.objects.filter(pk__lte=100).order_by("location")

class AllView(ListView):
    template_name = 'univermodel_list.html'
    queryset = UniverModel.objects.all()

class NoneView(ListView):
    template_name = 'univermodel_list.html'
    queryset = UniverModel.objects.none()

class ValuesView(ListView):
    template_name = 'univermodel_list.html'
    queryset = UniverModel.objects.filter(title="University of Oxford").values("id", "title", "overall")

    def get(self, request, *args, **kwargs):
        print(list(UniverModel.objects.all().values_list("id", "title")))
        return super().get(request, *args, **kwargs)




