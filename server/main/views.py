from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View, ListView, DetailView, DeleteView
from .models import User, NotiBoard, NotiBoardImage, AreaBoard, AreaBoardLike, AreaComment, AreaBoardImage
from .helper import jsonHelper

SUCCESS_URL = "/action?act=1"
FAIL_URL = "/action?act=0"

def intro(request):
    return HttpResponse("Intro")

class Action(View):

    def get(self, request):
        return jsonHelper.returnJson(jsonHelper.actionToJson(request.GET['act']))

class JoinUser(CreateView):
    model = User
    fields = ['google_token', 'nickname', 'email']

    def get_success_url(self):
        try:
            User.objects.get(google_token=self.object.google_token)
            return SUCCESS_URL
        except:
            return FAIL_URL

    def form_invalid(self, form): # 사용자 가입 실패할 경우 실패 페이지 호출
        return HttpResponseRedirect(FAIL_URL)

class LoginUser(View):
    model = User

    def post(self, request):
        try:
            user = User.objects.get(google_token=request.POST['google_token'])
            return jsonHelper.returnJson(jsonHelper.userInfoToJson(1, user.nickname))
        except:
            return jsonHelper.returnJson(jsonHelper.userInfoToJson(0, ""))

class NotiList(ListView):

    def get_queryset(self, paginate):
        return NotiBoard.objects.order_by('-created_at')[paginate*20:paginate*20+20]

    def get(self, request, paginate):
        if 'base' in request.GET and request.GET['base'] == '1':
            return jsonHelper.returnJson(jsonHelper.notiListToJson(
                NotiBoard.objects.order_by('-created_at')[0:1]
            ))

        return jsonHelper.returnJson(jsonHelper.notiListToJson(
            self.get_queryset(paginate)
        ))

class NotiDetail(DetailView):

    def get_queryset(self, id):
        noti_board = NotiBoard.objects.get(id=id)
        noti_board.images = NotiBoardImage.objects.filter(noti_id=id).order_by('order')
        return noti_board

    def get(self, request, id):
        return jsonHelper.returnJson(jsonHelper.notiToJson(
            self.get_queryset(id)
        ))

class NotiCreate(CreateView):
    model = NotiBoard
    fields = ['']

class AreaList(ListView):
    def get_queryset(self, area, paginate, base):
        if base == '0':
            areaBoards = AreaBoard.objects.filter(area_full_name=area).order_by('-created_at')[paginate*20:paginate*20+20]
        else:
            areaBoards = AreaBoard.objects.filter(area_full_name=area).order_by('-created_at')[0:2]

        for i in range(len(areaBoards)):
            areaBoards[i].like = len(AreaBoardLike.objects.filter(area_board_id=areaBoards[i].id))
            areaBoards[i].comment = len(AreaComment.objects.filter(area_board_id=areaBoards[i].id))
            areaBoards[i].writer_nickname = User.objects.get(id=areaBoards[i].user_id).nickname
        return areaBoards

    def get(self, request, area, paginate):
        if 'base' in request.GET and request.GET['base'] == '1':
            return jsonHelper.returnJson(jsonHelper.areaListToJson(
                self.get_queryset(area, 0, request.GET and request.GET['base'])
            ))

        return jsonHelper.returnJson(jsonHelper.areaListToJson(
            self.get_queryset(area, paginate, '0')
        ))

class AreaDetail(DetailView):

    def get_queryset(self, id):
        area_board = AreaBoard.objects.get(id=id)
        area_board.like = len(AreaBoardLike.objects.filter(area_board_id=area_board.id))
        area_board.comment = len(AreaComment.objects.filter(area_board_id=area_board.id))
        area_board.writer_nickname = User.objects.get(id=area_board.user_id).nickname
        area_board.images = AreaBoardImage.objects.filter(area_board_id=id).order_by('order')
        return area_board

    def get(self, request, id):
        return jsonHelper.returnJson(jsonHelper.areaToJson(
            self.get_queryset(id)
        ))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get("GOOGLETOKEN")).id == AreaBoard.objects.get(id=id).user_id:
            AreaBoard.objects.get(id=id).delete()
            AreaComment.objects.filter(area_board_id=id).delete()
            return jsonHelper.returnJson(jsonHelper.actionToJson(1))
        else:
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))


class AreaUpload(View):
    def post(self, request):
        data = request.POST
        try:
            areaBoard = AreaBoard.objects.create(user_id=User.objects.get(google_token=data['google_token']).id,
                                                 area_full_name=data['area_full_name'],
                                                 area_end_name=data['area_end_name'],
                                                 content=data['content'])
            areaBoard.like = 0
            areaBoard.comment = 0
            areaBoard.writer_nickname = User.objects.get(google_token=data['google_token']).nickname
        except:
            areaBoard = False

        return jsonHelper.returnJson(jsonHelper.areaUploadToJson(
            areaBoard
        ))

class AreaLike(View):
    def post(self, request, board_id):
        data = request.POST
        AreaBoardLike.objects.get_or_create(area_board_id=board_id,
                                user_id=User.objects.get(google_token=data['google_token']).id)

        return jsonHelper.returnJson(jsonHelper.countToJson(
            len(AreaBoardLike.objects.filter(area_board_id=board_id))))

class AreaCommentList(ListView):
    def get_queryset(self, board_id, paginate):
        areaCommentBoards = AreaComment.objects.filter(area_board_id=board_id, comment_group_id=0).order_by('created_at')[paginate*20:paginate*20+20]
        for i in range(len(areaCommentBoards)):
            areaCommentBoards[i].replys = AreaComment.objects.filter(comment_group_id=areaCommentBoards[i].id)
            areaCommentBoards[i].user = User.objects.get(id=areaCommentBoards[i].user_id)
            for j in range(len(areaCommentBoards[i].replys)):
                areaCommentBoards[i].replys[j].user = User.objects.get(id=areaCommentBoards[i].replys[j].user_id)
        return areaCommentBoards

    def get(self, request, board_id, paginate):
        return jsonHelper.returnJson(jsonHelper.areaCommentListToJson(
            self.get_queryset(board_id, paginate)
        ))

class AreaCommentView(View):
    def post(self, request, id):
        data = request.POST
        areaComment = AreaComment.objects.create(user_id=User.objects.get(google_token=data['google_token']).id,
                                                 area_board_id=id,
                                                 comment_group_id=data['group_id'] if 'group_id' in data else 0,
                                                 content=data['content'])
        areaComment.user = User.objects.get(id=areaComment.user_id)
        areaComment.replys = []

        return jsonHelper.returnJson(jsonHelper.areaCommentListToJson([areaComment]))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get('GOOGLETOKEN')).id == AreaComment.objects.get(id=id).user_id:
            AreaComment.objects.get(id=id).delete()
            AreaComment.objects.filter(comment_group_id=id).delete()
            return jsonHelper.returnJson(jsonHelper.actionToJson(1))
        else:
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))