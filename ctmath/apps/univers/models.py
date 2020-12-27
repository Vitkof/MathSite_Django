from django.db import models

class UniverModel(models.Model):
    title = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    overall = models.FloatField()
    teaching = models.FloatField()
    research = models.FloatField()
    citations = models.FloatField()
    industry_income = models.FloatField()
    international_outlook = models.FloatField()
    number_students = models.PositiveIntegerField()
    students_staff = models.FloatField()
    percent_foreigners = models.PositiveSmallIntegerField()
    gender_ratio = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.id}_{self.title}"
