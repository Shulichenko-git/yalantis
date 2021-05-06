from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, blank=False)
    date_of_start = models.DateField(blank=False, editable=True)
    date_of_finish = models.DateField(blank=False, editable=True)
    number_of_lectures = models.IntegerField()
