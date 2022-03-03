from dataclasses import fields
from django import forms
from .models import Article

class ArticleFrom(forms.ModelForm):
  class Meta:
    model = Article
    fields = ["title", "content", "article_image"]