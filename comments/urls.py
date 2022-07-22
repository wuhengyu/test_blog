from django.urls import path
from . import views

# 指定命名空间
app_name = 'comments1'
urlpatterns = [
    path('comment/post/<int:blog_pk>/', views.blog_comment, name='blog_comment'),
]
