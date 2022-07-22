from django import forms
from .models import Comment


# 继承于forms.ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        # 指定数据模型
        model = Comment
        fields = ['text']
