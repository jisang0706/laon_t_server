from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View, ListView, DetailView, DeleteView
from .models import User, NotiBoard, NotiBoardImage, AreaBoard, AreaBoardLike, AreaComment, AreaBoardImage, \
    PlaygroundBoard, PlaygroundBoardLike, PlaygroundComment, PlaygroundBoardImage
from .helper import jsonHelper

SUCCESS_URL = "/action?act=1"
FAIL_URL = "/action?act=0"

def intro(request):
    return HttpResponse("Intro")

class Action(View):

    def get(self, request):
        return jsonHelper.returnJson(jsonHelper.actionToJson(request.GET['act']))

class JoinUser(View):

    def post(self, request):
        data = request.POST
        if len(User.objects.filter(nickname=data['nickname'])) > 0:
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))
        User.objects.create(google_token=data['google_token'], nickname=data['nickname'], email=data['email'])
        return jsonHelper.returnJson(jsonHelper.actionToJson(1))

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

class setNickname(View):
    def post(self, request):
        new_nickname = request.POST.get('nickname')
        if (len(User.objects.filter(nickname=new_nickname)) > 0):
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))

        user = User.objects.get(google_token=request.headers.get('GOOGLETOKEN'))
        user.nickname = new_nickname
        user.save()
        return jsonHelper.returnJson(jsonHelper.actionToJson(1))

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
    def get_queryset(self, area, paginate, base, search):
        if base == '0':
            areaBoards = AreaBoard.objects.filter(area_full_name=area).order_by('-created_at')[paginate*20:paginate*20+20]
        elif base == '2':
            areaBoards = AreaBoard.objects.filter(
                Q(area_full_name=area) & Q(content__icontains=search)
            ).order_by('-created_at')[paginate*20:paginate*20+20]
        else:
            areaBoards = AreaBoard.objects.filter(area_full_name=area).order_by('-created_at')[0:2]

        for i in range(len(areaBoards)):
            areaBoards[i].like = len(AreaBoardLike.objects.filter(area_board_id=areaBoards[i].id))
            areaBoards[i].comment = len(AreaComment.objects.filter(area_board_id=areaBoards[i].id))
            try:
                areaBoards[i].writer_nickname = User.objects.get(id=areaBoards[i].user_id).nickname
            except:
                areaBoards[i].writer_nickname = ""
        return areaBoards

    def get(self, request, area, paginate):
        if 'base' in request.GET and request.GET['base'] == '1':
            return jsonHelper.returnJson(jsonHelper.boardListToJson(
                self.get_queryset(area, 0, '1', '')
            ))

        if 'search' in request.GET:
            return jsonHelper.returnJson(jsonHelper.boardListToJson(
                self.get_queryset(area, paginate, '2', request.GET['search'])
            ))

        return jsonHelper.returnJson(jsonHelper.boardListToJson(
            self.get_queryset(area, paginate, '0', '')
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
        return jsonHelper.returnJson(jsonHelper.boardToJson(
            self.get_queryset(id)
        ))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get("GOOGLETOKEN")).id == AreaBoard.objects.get(id=id).user_id:
            AreaBoard.objects.get(id=id).delete()
            AreaComment.objects.filter(area_board_id=id).delete()
            AreaBoardLike.objects.filter(area_board_id=id).delete()
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

        return jsonHelper.returnJson(jsonHelper.boardUploadToJson(
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
        return jsonHelper.returnJson(jsonHelper.commentListToJson(
            self.get_queryset(board_id, paginate)
        ))

class AreaCommentView(View):
    def post(self, request, id):
        data = request.POST
        areaComment = AreaComment.objects.create(user_id=User.objects.get(google_token=data['google_token']).id,
                                                 area_board_id=id,
                                                 comment_group_id=data['group_id'] if 'group_id' in data else 0,
                                                 content=data['content'])
        if (int(areaComment.comment_group_id) != 0):
            print(areaComment.comment_group_id)
            areaComment = AreaComment.objects.get(id=areaComment.comment_group_id)
        areaComment.user = User.objects.get(id=areaComment.user_id)
        areaComment.replys = list(AreaComment.objects.filter(comment_group_id=areaComment.id))
        for i in range(len(areaComment.replys)):
            areaComment.replys[i].user = User.objects.get(id=areaComment.replys[i].user_id)

        return jsonHelper.returnJson(jsonHelper.commentListToJson([areaComment]))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get('GOOGLETOKEN')).id == AreaComment.objects.get(id=id).user_id:
            AreaComment.objects.get(id=id).delete()
            AreaComment.objects.filter(comment_group_id=id).delete()
            return jsonHelper.returnJson(jsonHelper.actionToJson(1))
        else:
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))

class PGList(ListView):
    def get_queryset(self, pg_name, paginate, base, search):
        if base == '0':
            pgBoards = PlaygroundBoard.objects.filter(playground_name=pg_name).order_by('-created_at')[paginate*20:paginate*20+20]
        elif base == '2':
            pgBoards = PlaygroundBoard.objects.filter(
                Q(playground_name=pg_name) & Q(content__icontains=search)
            ).order_by('-created_at')[paginate*20:paginate*20+20]
        else:
            pgBoards = [PlaygroundBoard.objects.filter(playground_name=pg_name).latest('id')]

        for i in range(len(pgBoards)):
            pgBoards[i].like = len(PlaygroundBoardLike.objects.filter(playground_board_id=pgBoards[i].id))
            pgBoards[i].comment = len(PlaygroundComment.objects.filter(playground_board_id=pgBoards[i].id))
            try:
                pgBoards[i].writer_nickname = User.objects.get(id=pgBoards[i].user_id).nickname
            except:
                pgBoards[i].writer_nickname = ""
        return pgBoards

    def get(self, request, pg_name, paginate):
        if 'base' in request.GET and request.GET['base'] == '1':
            return jsonHelper.returnJson(jsonHelper.boardListToJson(
                self.get_queryset(pg_name, 0, '1', '')
            ))

        if 'search' in request.GET:
            return jsonHelper.returnJson(jsonHelper.boardListToJson(
                self.get_queryset(pg_name, paginate, '2', request.GET['search'])
            ))

        return jsonHelper.returnJson(jsonHelper.boardListToJson(
            self.get_queryset(pg_name, paginate, '0', '')
        ))

class PGDetail(DetailView):
    def get_queryset(self, id):
        pg_board = PlaygroundBoard.objects.get(id=id)
        pg_board.like = len(PlaygroundBoardLike.objects.filter(playground_board_id=pg_board.id))
        pg_board.comment = len(PlaygroundComment.objects.filter(playground_board_id=pg_board.id))
        pg_board.writer_nickname = User.objects.get(id=pg_board.user_id).nickname
        pg_board.images = PlaygroundBoardImage.objects.filter(playground_board_id=pg_board.id).order_by('order')
        return pg_board

    def get(self, request, id):
        return jsonHelper.returnJson(jsonHelper.boardToJson(
            self.get_queryset(id)
        ))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get('GOOGLETOKEN')).id == PlaygroundBoard.objects.get(id=id).user_id:
            PlaygroundBoard.objects.get(id=id).delete()
            PlaygroundComment.objects.filter(playground_board_id=id).delete()
            PlaygroundBoardLike.objects.filter(playground_board_id=id).delete()
            return jsonHelper.returnJson(jsonHelper.actionToJson(1))
        else:
            return jsonHelper.returnJson(jsonHelper.actionToJson(0))

class PGUpload(View):
    def post(self, request):
        data = request.POST
        try:
            pgBoard = PlaygroundBoard.objects.create(user_id=User.objects.get(google_token=data['google_token']).id,
                                                     playground_name=data['playground_name'],
                                                     content=data['content'])
            pgBoard.like = 0
            pgBoard.comment = 0
            pgBoard.writer_nickname = User.objects.get(google_token=data['google_token']).nickname
        except:
            pgBoard = False

        return jsonHelper.returnJson(jsonHelper.boardUploadToJson(
            pgBoard
        ))

class PGLike(View):
    def post(self, request, board_id):
        data = request.POST
        PlaygroundBoardLike.objects.get_or_create(playground_board_id=board_id,
                                                  user_id=User.objects.get(google_token=data['google_token']).id)

        return jsonHelper.returnJson(jsonHelper.countToJson(
            len(PlaygroundBoardLike.objects.filter(playground_board_id=board_id))
        ))

class PGCommentList(ListView):
    def get_queryset(self, board_id, paginate):
        pgCommentBoards = PlaygroundComment.objects.filter(playground_board_id=board_id, comment_group_id=0).order_by('created_at')[paginate*20:paginate*20+20]
        for i in range(len(pgCommentBoards)):
            pgCommentBoards[i].replys = PlaygroundComment.objects.filter(comment_group_id=pgCommentBoards[i].id)
            pgCommentBoards[i].user = User.objects.get(id=pgCommentBoards[i].user_id)
            for j in range(len(pgCommentBoards[i].replys)):
                pgCommentBoards[i].replys[j].user = User.objects.get(id=pgCommentBoards[i].replys[j].user_id)
        return pgCommentBoards

    def get(self, request, board_id, paginate):
        return jsonHelper.returnJson(jsonHelper.commentListToJson(
            self.get_queryset(board_id, paginate)
        ))

class PGCommentView(View):
    def post(self, request, id):
        data = request.POST
        pgComment = PlaygroundComment.objects.create(user_id=User.objects.get(google_token=data['google_token']).id,
                                                     playground_board_id=id,
                                                     comment_group_id=data['group_id'] if 'group_id' in data else 0,
                                                     content=data['content'])
        if (int(pgComment.comment_group_id) != 0):
            pgComment = PlaygroundComment.objects.get(id=pgComment.comment_group_id)
        pgComment.user = User.objects.get(id=pgComment.user_id)
        pgComment.replys = list(PlaygroundComment.objects.filter(comment_group_id=pgComment.id))
        for i in range(len(pgComment.replys)):
            pgComment.replys[i].user = User.objects.get(id=pgComment.replys[i].user_id)

        return jsonHelper.returnJson(jsonHelper.commentListToJson([pgComment]))

    def delete(self, request, id):
        if User.objects.get(google_token=request.headers.get('GOOGLETOKEN')).id == PlaygroundComment.objects.get(id=id).user_id:
            PlaygroundComment.objects.get(id=id).delete()
            PlaygroundComment.objects.filter(comment_group_id=id).delete()
            return jsonHelper.returnJson(jsonHelper.actionToJson(1))
        return jsonHelper.returnJson(jsonHelper.actionToJson(0))