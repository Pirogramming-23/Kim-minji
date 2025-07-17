from django.urls import path
from . import views

app_name = 'devtools'

urlpatterns = [
    path('', views.devtool_list, name='devtool_list'),                       # 개발툴 리스트
    path('add/', views.devtool_add, name='devtool_add'),                    # 개발툴 등록
    path('<int:pk>/', views.devtool_detail, name='devtool_detail'),         # 개발툴 상세
    path('<int:pk>/edit/', views.devtool_edit, name='devtool_edit'),        # 개발툴 수정
    path('<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),  # 개발툴 삭제
]
