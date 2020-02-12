from django.urls import path
from . import views

urlpatterns = [
    #path('', views.BaseView.as_view(), name='home'),
    path('', views.PostList.as_view(), name='home'),
    #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    #path('categories/', views.CategoryList.as_view(), name='category_list'),
    #path('', views.category_list, name='category_list'),
    path('categorias/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
] 
