from django.contrib import admin
from .models import Quote, Comment, Like

# Register your models here.
admin.site.register(Quote)
admin.site.register(Comment)
admin.site.register(Like)

