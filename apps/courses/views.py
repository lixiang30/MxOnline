from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger # 分页功能需要导入的类

from .models import Course
from operation.models import UserFavorite


class CourseListView(View):
    """
    课程列表页
    """
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 　对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request,"course-list.html",{
            "all_courses":courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })

class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程点击加１
        course.click_nums += 1
        course.save()

        # 通过当前标签，查找数据库中的课程
        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag =course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request,"course-detail.html",{
            "course":course,
            "relate_courses":relate_courses,
        })



class CourseInfoView(View):
    """
    课程章节
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request,"course-video.html",{
            "course":course,
        })




