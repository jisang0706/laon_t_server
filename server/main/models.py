from django.db import models

class User(models.Model):
    google_token = models.TextField()
    nickname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

"""=========================================================================="""

class NotiBoard(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class NotiBoardImage(models.Model):
    noti_id = models.IntegerField()
    order = models.IntegerField()
    img_link = models.CharField(max_length=50)

"""=========================================================================="""

class PlaygroundBoard(models.Model):
    user_id = models.IntegerField()
    playground_name = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PlaygroundBoardImage(models.Model):
    playground_board_id = models.IntegerField()
    order = models.IntegerField()
    img_link = models.CharField(max_length=50)

class PlaygroundBoardLike(models.Model):
    playground_board_id = models.IntegerField()
    user_id = models.IntegerField()

class PlaygroundBoardReport(models.Model):
    playground_board_id = models.IntegerField()
    user_id = models.IntegerField()

class PlaygroundComment(models.Model):
    playground_board_id = models.IntegerField()
    user_id = models.IntegerField()
    comment_group_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PlaygroundCommentReport(models.Model):
    playground_comment_id = models.IntegerField()
    user_id = models.IntegerField()

"""=========================================================================="""

class AreaBoard(models.Model):
    user_id = models.IntegerField()
    area_full_name = models.CharField(max_length=50)
    area_end_name = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AreaBoardImage(models.Model):
    area_board_id = models.IntegerField()
    order = models.IntegerField()
    img_link = models.CharField(max_length=50)

class AreaBoardLike(models.Model):
    area_board_id = models.IntegerField()
    user_id = models.IntegerField()

class AreaBoardReport(models.Model):
    area_board_id = models.IntegerField()
    user_id = models.IntegerField()

class AreaComment(models.Model):
    area_board_id = models.IntegerField()
    user_id = models.IntegerField()
    comment_group_id = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AreaCommentReport(models.Model):
    area_comment_id = models.IntegerField()
    user_id = models.IntegerField()