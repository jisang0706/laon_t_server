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

def boardListToJson(boards):
    output = {
        'meta': {
            'size': len(boards)
        },
        'list': [{
            'id': board.id,
            'content': board.content[:15] + '...' if len(board.content) >= 15 else board.content,
            'created_at': board.created_at.strftime("%Y.%m.%d %H:%M"),
            'like': board.like,
            'comment': board.comment,
            'writer_nickname': board.writer_nickname
        } for board in boards]
    }
    return output

def boardToJson(boards):
    output = {
        'id' : boards.id,
        'created_at' : boards.created_at.strftime("%Y.%m.%d %H:%M"),
        'content' : boards.content,
        'like' : boards.like,
        'comment' : boards.comment,
        'writer_nickname' : boards.writer_nickname
    }

    try:
        output['images'] = [img.img_link for img in boards.images]
    except:
        output['images'] = []

    return output

def boardUploadToJson(boards):
    if boards == False:
        output = {
            'id': 0
        }
    else:
        output = {
            'id' : boards.id
        }
    return output

def countToJson(cnt):
    output = {
        'count': cnt
    }
    return output

def commentListToJson(comment_boards):
    output = {
        'meta': {
            'size': len(comment_boards)
        },
        'list': [{
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.strftime("%Y.%m.%d %H:%M"),
            'writer_nickname': comment.user.nickname,
            'reply': [{
                'id': reply.id,
                'content': reply.content,
                'created_at': reply.created_at.strftime("%Y.%m.%d %H:%M"),
                'writer_nickname': reply.user.nickname,
            } for reply in comment.replys]
        } for comment in comment_boards]
    }

    return output