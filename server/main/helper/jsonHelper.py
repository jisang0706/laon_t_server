from django.http import JsonResponse

def returnJson(content):
    return JsonResponse(content, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def actionToJson(action):
    output = {
        'action': action
    }
    return output

def userInfoToJson(action, nickname):
    output = actionToJson(action)
    output['nickname'] = nickname
    return output

def notiListToJson(noti_boards):
    output = {
        'meta' : {
            'size' : len(noti_boards)
        },
        'list' : [{
            'id' : noti.id,
            'title' : noti.title,
            'created_at' : noti.created_at.strftime("%Y.%m.%d %H:%M"),
        } for noti in noti_boards]
    }
    return output

def notiToJson(noti_board):
    output = {
        'id' : noti_board.id,
        'title' : noti_board.title,
        'created_at' : noti_board.created_at.strftime("%Y.%m.%d %H:%M"),
        'content' : noti_board.content
    }

    try:
        output['images'] = [img.img_link for img in noti_board.images]
    except:
        output['images'] = []

    return output

def areaListToJson(area_boards):
    output = {
        'meta': {
            'size': len(area_boards)
        },
        'list': [{
            'id': area.id,
            'content': area.content[:15] + '...' if len(area.content) >= 15 else area.content,
            'created_at': area.created_at.strftime("%Y.%m.%d %H:%M"),
            'like': area.like,
            'comment': area.comment,
            'writer_nickname': area.writer_nickname
        } for area in area_boards]
    }
    return output

def areaToJson(area_board):
    output = {
        'id' : area_board.id,
        'created_at' : area_board.created_at.strftime("%Y.%m.%d %H:%M"),
        'content' : area_board.content,
        'like' : area_board.like,
        'comment' : area_board.comment,
        'writer_nickname' : area_board.writer_nickname
    }

    try:
        output['images'] = [img.img_link for img in area_board.images]
    except:
        output['images'] = []

    return output

def areaUploadToJson(area_board):
    if area_board == False:
        output = {
            'action': 0,
            'id': 0,
            'created_at': '0',
            'content': '',
            'like': 0,
            'comment': 0,
            'writer_nickname': ''
        }
    else:
        output = {
            'action': 1,
            'id' : area_board.id,
            'created_at' : area_board.created_at.strftime("%Y.%m.%d %H:%M"),
            'content' : area_board.content,
            'like' : area_board.like,
            'comment' : area_board.comment,
            'writer_nickname': area_board.writer_nickname
        }
    return output

def countToJson(cnt):
    output = {
        'count': cnt
    }
    return output

def areaCommentListToJson(area_comment_boards):
    output = {
        'meta': {
            'size': len(area_comment_boards)
        },
        'list': [{
            'id': area_comment.id,
            'content': area_comment.content,
            'created_at': area_comment.created_at.strftime("%Y.%m.%d %H:%M"),
            'writer_nickname': area_comment.user.nickname,
            'reply': [{
                'id': reply.id,
                'content': reply.content,
                'created_at': reply.created_at.strftime("%Y.%m.%d %H:%M"),
                'writer_nickname': reply.user.nickname,
            } for reply in area_comment.replys]
        } for area_comment in area_comment_boards]
    }

    return output