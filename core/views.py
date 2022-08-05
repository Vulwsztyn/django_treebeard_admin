from django.shortcuts import render
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Manager
from django.views.generic import ListView
from models import Person, Course, Grade
# Create your views here.
# class PersonList(ListView):
#     model = Person
#     context_object_name = "people"
#     queryset = Person.objects.prefetch_related("courses").annotate(grade_avg=Avg("courses__grade__grade"))