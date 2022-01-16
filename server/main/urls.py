from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro, name='index'),
    path('action', views.Action.as_view()),
    path('user/join', views.JoinUser.as_view()),
    path('user/login', views.LoginUser.as_view()),
    path('noti/list/<int:paginate>', views.NotiList.as_view()),
    path('noti/<int:id>', views.NotiDetail.as_view()),
]