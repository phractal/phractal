"""kanban URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from django.contrib import admin
from django.urls import path, include
from nodes import views as node_views

from nodes.views import HeartViewSet, NodeOpViewSet, NodeCreateViewSet, NodeDownLoadViewSet, NodeTypeViewSet, \
    Node_Management_List, NodeNumManageViewSet, NodeRunManageViewSet, NodeStatistic, IndividualStatistic, \
    AllDownloadNode, \
    AlreadyDownloadNode, Statistics, Set_cpu_or_mem

from tasks import views as task_views
from accounts import views as account_views
from wallets import views as wallet_views
from index.views import IndexView, LoginView, RegisterView, TaskpubView, ParticularView, TasklistView, MyorderView, \
    PersonaldataView, MynodeView, ChangepasswdView, WalletView, StatisticsView, \
    DownloadView, BlockChainView, SearchHistoryView, SearchResultView, SearchResultSelectedView, \
    SearchResultSelectedDetailView, MapView, TypeNodeView, SearchNodeView

from accounts.views import TestView, UserProfileView, WechatBound, WeiXinQRLogin, Authorization
from wallets.views import WxPayNotifyView, WithdrawView


router = DefaultRouter()
router.register("node", node_views.NodeViewSet, base_name="node")

# router.register('node_heart', node_views.HeartViewSet, base_name='order')


router.register("tasknode", node_views.TaskNodeViewsSet, base_name="tasknode")
router.register("task", task_views.TaskViewSets, base_name="task")
router.register("phonecode", account_views.PhoneMessageViewSet, base_name="phonecode")
router.register("register/phone", account_views.RegisterViewSet, base_name="register/phone")
router.register("register/simple", account_views.RegisterViewSet, base_name="register/simple")
router.register("payment", wallet_views.PaymentViewSets, base_name="payment")
router.register("myaccount", wallet_views.MyAccountViewSets, base_name="myaccount")
# router.register("noderevenuerecord", wallet_views.NodeRevenueRecordViewSets, base_name="noderevenuerecord")




urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),



    path("api-token-auth/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api-token-refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api-token-verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),




    path("node_heart/", HeartViewSet.as_view()),
    path("test/", TestView.as_view()),
    path("index/", IndexView.as_view()),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),

    path("taskpub/", TaskpubView.as_view()),
    path("tasklist/", TasklistView.as_view()),
    path("myorder/", MyorderView.as_view()),
    path("personaldata/", PersonaldataView.as_view()),
    path("mynode/", MynodeView.as_view()),
    path("changepasswd/", ChangepasswdView.as_view()),
    path("wallet/", WalletView.as_view()),
    # path("node_num_manage/", NodeNumManageViewSet.as_view()),
    path("node_run_manage/", NodeRunManageViewSet.as_view()),
    # path("node_num_manage/", NodeNumManageViewSet.as_view()),
    path("node_num_manage/", Node_Management_List.as_view()),
    path("particular/", ParticularView.as_view()),
    path("userprofile/", UserProfileView.as_view()),
    path("wx_notify/", WxPayNotifyView.as_view()),
    path("withdraw/", WithdrawView.as_view()),
    path("bound/", WechatBound.as_view()),

    path("node_operate/", NodeOpViewSet.as_view()),

    path("create_node/", NodeCreateViewSet.as_view()),
    path("download/", NodeDownLoadViewSet.as_view()),
    path("nodetype/", NodeTypeViewSet.as_view()),
    path("node_management_list/", Node_Management_List.as_view()),


    path("weixinqrlogin/", WeiXinQRLogin.as_view()),
    path("authorization/", Authorization.as_view()),
    path("statistics/", StatisticsView.as_view()),
    path("globalstatistic/", NodeStatistic.as_view()),
    path("individualstatistic/", IndividualStatistic.as_view()),
    path("download_node/", DownloadView.as_view()),
    path("all_download_node/", AllDownloadNode.as_view()),
    path("already_download_node/", AlreadyDownloadNode.as_view()),
    path("blockchain/", BlockChainView.as_view()),

    path("blocktask/", task_views.BlockTaskView.as_view()),
    path("blocktaskdetail/", task_views.BlockTaskDetail.as_view()),

    path("updateblocktask/", task_views.UpdateBlockTask.as_view()),
    path("block/", task_views.BlockView.as_view()),
    path("blockdetail/", task_views.BlockDetail.as_view()),
    path("updateblock/", task_views.UpdateBlock.as_view()),

    path("blockacount/", task_views.BlockAcountView.as_view()),
    path("blockacountdetail/", task_views.BlockAcountDetailView.as_view()),
    path("miner/", task_views.BlockMinerView.as_view()),
#节点检索及统计查询

    # path("statistics_query/", Statistics.as_view()),

    path("statistics_query/", Statistics.as_view()),

    path("set_cpu_or_mem/", Set_cpu_or_mem.as_view()),



    # 搜索
    path("search_history/", SearchHistoryView.as_view()),
    path("map/", MapView.as_view()),
    path("type_to_node/", TypeNodeView.as_view()),
    path("search_node/", SearchNodeView.as_view()),
    path("search_result/", SearchResultView.as_view()),
    path("search_result_selected/", SearchResultSelectedView.as_view()),
    path("search_result_selected_detail/", SearchResultSelectedDetailView.as_view()),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     schema_view = get_schema_view(
#         openapi.Info(
#             title='任务抓取看板 API',
#             default_version='v0.1',
#             description='任务抓取平台看板server API 文档',
#             terms_of_service='',
#             contact=openapi.Contact(email='000000000@qq.com'),
#             license=openapi.License(name=''),
#         ),
#         public=True,
#     )
#     urlpatterns += [path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')]
#     urlpatterns += [path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')]
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
