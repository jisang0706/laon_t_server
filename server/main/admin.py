from django.contrib import admin
from .models import User, NotiBoard, NotiBoardImage,\
    PlaygroundBoard, PlaygroundBoardImage, PlaygroundBoardLike, PlaygroundBoardReport,\
    PlaygroundComment, PlaygroundCommentReport,\
    AreaBoard, AreaBoardImage, AreaBoardLike, AreaBoardReport,\
    AreaComment, AreaCommentReport

admin.site.register(User)
admin.site.register(NotiBoard)
admin.site.register(NotiBoardImage)
admin.site.register(PlaygroundBoard)
admin.site.register(PlaygroundBoardImage)
admin.site.register(PlaygroundBoardLike)
admin.site.register(PlaygroundBoardReport)
admin.site.register(PlaygroundComment)
admin.site.register(PlaygroundCommentReport)
admin.site.register(AreaBoard)
admin.site.register(AreaBoardImage)
admin.site.register(AreaBoardLike)
admin.site.register(AreaBoardReport)
admin.site.register(AreaComment)
admin.site.register(AreaCommentReport)