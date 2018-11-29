from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger # 分页功能需要导入的类
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course
from operation.models import UserFavorite

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        all_orgs = CourseOrg.objects.all()

        all_citys = CityDict.objects.all()
        #　取出筛选城市
        city_id = request.GET.get('city',"")

        # 根据点击量对热门机构进行筛选，列出排名前五的机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        #根据城市进行筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)

        #
        sort = request.GET.get('sort','')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 机构数统计
        org_nums = all_orgs.count()

        #　对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,5,request=request)

        orgs = p.page(page)


        return render(request,"org-list.html",{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':{0}}".format(userask_form.errors),content_type='application/json')
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            # return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # ===============判断收藏状态============================
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            "current_page":current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers':all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })

class AddFavView(View):
    """
    用户收藏、取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        #　判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse("{'status':'fail','msg':'用户未登陆'}",content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request,fav_id=int(fav_id),fav_type=fav_type)
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            return HttpResponse("{'status':'fail','msg':'收藏'}", content_type="application/json")
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse("{'status':'success','msg':'已收藏'}", content_type="application/json")
            else:
                return HttpResponse("{'status':'fail','msg':'收藏出错'}",content_type="application/json")
