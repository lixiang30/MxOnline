import xadmin
from .models import EmailVerifyRecord,Banner

class EmailVerifyRecordAdmin(object):
    # 显示的字段
    list_display = ['code','email','send_type','send_time']
    # 搜索字段
    search_fields = ['code','email','send_type']
    # 过滤字段
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index','add_time']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)