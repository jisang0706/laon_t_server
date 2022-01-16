from django.http import JsonResponse

def returnJson(content):
    return JsonResponse(content, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)

def actionToJson(action):
    output = {
        'action': action
    }
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
        'content' : noti_board.content,
        'images' : [img.img_link for img in noti_board.images]
    }
    return output