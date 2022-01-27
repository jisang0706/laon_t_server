from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View, ListView, DetailView
from .models import User, NotiBoard, NotiBoardImage
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
            return jsonHelper.returnJson(jsonHelper.userInfoToJson(True, user.nickname))
        except:
            return jsonHelper.returnJson(jsonHelper.userInfoToJson(False, ""))

class NotiList(ListView):

    def get_queryset(self, paginate):
        return NotiBoard.objects.order_by('-created_at')[paginate*20:paginate*20+20]

    def get(self, request, paginate):
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