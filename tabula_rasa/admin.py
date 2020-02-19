from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from .models import Category
from .models import Comment
from .models import Introduction
from .models import Post
from .models import User


class PostModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        'content': {'widget': AdminMarkdownxWidget},
    }



admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Comment, PostModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Introduction)
