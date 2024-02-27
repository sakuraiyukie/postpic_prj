from django.urls import path

from . import views


app_name = 'picture'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post/', views.CreatePictureView.as_view(), name="post"),
    path('post_done/', views.PostSuccessView.as_view(), name="post_done"),
    path('picture/<int:category>', views.CategoryView.as_view(), name="picture_cat"),
    path('user-list/<int:user>', views.UserView.as_view(), name='user_list'),
    path('picture-detail/<int:pk>', views.DetailView.as_view(), name = 'picture_detail'),
    path('mypage/', views.MypageView.as_view(), name="mypage"),
    path('picture/<int:pk>/delete/', views.PictureDeleteView.as_view(), name="picture_delete"),
]




