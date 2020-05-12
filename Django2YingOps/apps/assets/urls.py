"""Django2YingOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from users.views import *
from assets.views import *


app_name = 'assets'
urlpatterns = [
    # path('admin/', admin.site.urls),
    # 初始化资产
    path('init/', AssetsInit.as_view(),name='assets_init'),
    # 资产列表
    path('list/', AssetsListView.as_view(),name='assets_list'),
    # 资产API
    path('listapi/', AssetsListApiView.as_view(),name='assets_listapi'),
    # 资产详情
    path('detail/<int:id>', AssetsDetailView.as_view(),name='assets_detail'),
    # 资产在线状态
    path('live_status/', csrf_exempt(AssetsLiveStatuslView.as_view()),name='assets_live_status'),
    # 资产全部更新
    path('updateassets/', csrf_exempt(UpdateAllAssetsView.as_view()),name='assets_update_all'),
    # 导出资产
    path('excleexport/', AssetsExportView.as_view(), name='assets_excle_export'),
    # webssh
    path('websshs/', AssetsWebSshsView.as_view(),name='assets_webssh'),
    # ipscan
    path('ipscan/', IpScanView.as_view(),name='assets_ipscan'),

    # ibm_status
    path('ibm_status/', csrf_exempt(IbmStatusView.as_view()),name='ibm_status'),


]
