from django import forms
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.widgets import MarkdownxWidget

from .models import Category
from .models import Comment
from .models import Introduction
from .models import Post


class SearchForm(forms.Form):
    text = forms.CharField(label="検索", required=True, )


class PostModel(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {
            'content': AdminMarkdownxWidget,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'content',)
        widgets = {
            'content': MarkdownxWidget(attrs={'class': 'com-form'}),
        }


class IntroductionForm(forms.ModelForm):
    class Meta:
        model = Introduction
        fields = ('introduction',)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post', 'category', 'content', 'is_public',)
        widgets = {
            'content': MarkdownxWidget(attrs={'class': 'post-form'}),
        }


class CreateCateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('kind',)
        