from django.contrib import admin
from .models import Quote, Comment, Like, SubComment

# Register your models here.
admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SubComment)

