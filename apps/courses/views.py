from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .models import Course


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all()
        return render(request,"course-list.html",{
            "all_courses":all_courses,
        })
