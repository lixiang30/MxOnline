from django.shortcuts import render

# Create your views here.
from django.views.generic import View


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        return render(request,"org-list.html",{})
