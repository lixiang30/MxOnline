import xadmin
from .models import EmailVerifyRecord,Banner
from xadmin import views

# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '在线教育后台管理系统'
    # 修改footer
    site_footer = '在线教育平台'
    # 收起菜单
    menu_style = 'accordion'


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

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)
