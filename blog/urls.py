from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    #path('', views.post_list, name="post_list"),
    path('', views.PostListView.as_view(), name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name="post_detail"),
    path('<int:post_id>/share/', views.post_share, name="post_share"),
    path('register', views.register, name="register"),
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('writeblog', views.writeblog, name="writeblog"),
]
