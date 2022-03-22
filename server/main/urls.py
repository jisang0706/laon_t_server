from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro, name='index'),
    path('action', views.Action.as_view()),
    path('user/join', views.JoinUser.as_view()), # 회원가입
    path('user/login', views.LoginUser.as_view(), name='userLogin'), # 로그인
    path('user/nickname', views.setNickname.as_view()), # 닉네임 변경
    path('user/area/<int:paginate>', views.AreaWritedList.as_view()), # 작성한 동네 글 리스트
    path('user/area/comment/<int:paginate>', views.AreaCommentWritedList.as_view()), # 작성한 동네 댓글 글 리스트
    path('user/playground/<int:paginate>', views.PGWritedList.as_view()), # 작성한 놀이터 글 리스트
    path('user/playground/comment/<int:paginate>', views.PGCommentWritedList.as_view()), # 작성한 놀이터 댓글 글 리스트

    path('noti/list/<int:paginate>', views.NotiList.as_view()), # 공지 리스트
    path('noti/<int:id>', views.NotiDetail.as_view()), # 공지글 상세

    path('area/<area>/<int:paginate>', views.AreaList.as_view()), # 동네 글 리스트,
    path('area/upload', views.AreaUpload.as_view()), # 동네 들 업로드
    path('area/<int:id>', views.AreaDetail.as_view(), name='areaDetail'), # 동네 글 상세, 삭제
    path('area/<int:board_id>/like', views.AreaLike.as_view()), # 동네 글 좋아요
    path('area/<int:board_id>/comment/<int:paginate>', views.AreaCommentList.as_view()), # 동네 댓글 리스트
    path('area/<int:id>/comment', views.AreaCommentView.as_view()), # 동네 댓글 업로드, 삭제
    path('area/<int:id>/name', views.AreaBoardName.as_view()), # 동네 글 동네명

    path('playground/<pg_name>/<int:paginate>', views.PGList.as_view()), # 놀이터 글 리스트
    path('playground/upload', views.PGUpload.as_view(), name='pgDetail'), # 놀이터 글 업로드
    path('playground/<int:id>', views.PGDetail.as_view()), # 놀이터 글 상세, 삭제
    path('playground/<int:board_id>/like', views.PGLike.as_view()), # 놀이터 글 좋아요
    path('playground/<int:board_id>/comment/<int:paginate>', views.PGCommentList.as_view()), # 놀이터 댓글 리스트
    path('playground/<int:id>/comment', views.PGCommentView.as_view()), # 놀이터 댓글 업로드, 삭제
    path('playground/<int:id>/name', views.PGBoardName.as_view()),  # 놀이터 글 놀이터명
]