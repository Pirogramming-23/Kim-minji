from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'ideas'

urlpatterns = [
    path('', views.idea_list, name='idea_list'),                       # 메인 페이지
    path('add/', views.idea_add, name='idea_add'),                    # 아이디어 등록
    path('<int:pk>/', views.idea_detail, name='idea_detail'),         # 아이디어 상세
    path('<int:pk>/edit/', views.idea_edit, name='idea_edit'),        # 아이디어 수정
    path('<int:pk>/delete/', views.idea_delete, name='idea_delete'),  # 아이디어 삭제
    path('<int:pk>/star/', views.idea_star, name='idea_star'),        # 아이디어 찜 AJAX
    path('<int:pk>/interest/', views.idea_interest, name='idea_interest'),  # 관심도 AJAX
    path('ajax_search/', views.ajax_search, name='ajax_search'),
] 
