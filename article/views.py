from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import ArticleFrom
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def articles(request):
  # Arama işlemi
  keyword = request.GET.get("keyword")
  if keyword:
    articles = Article.objects.filter(title__contains = keyword)
    return render(request, "articles.html", {"articles":articles})
  # Arama işlemi sonu
  
  articles = Article.objects.all()
  return render(request, "articles.html", {"articles":articles})
  
# Create your views here.
def index(request):
  return render(request, "index.html")

def about(request):
  return render(request, "about.html" )

@login_required(login_url="user:login")
def dashboard(request):
  articles = Article.objects.filter(author = request.user)
  context = {"articles" : articles}
  return render(request, "dashboard.html", context)

@login_required(login_url="user:login")
def add_article(request):
  form = ArticleFrom(request.POST or None, request.FILES or None)
  if form.is_valid():
    article = form.save(commit = False)
    article.author = request.user
    article.save()
    messages.success(request, "Makale başarıyla oluşturuldu.")
    return redirect("article:dashboard")
  else:    
    return render(request, "add_article.html", {"form" : form})

def detail(request, id):
  # article = Article.objects.filter(id = id).first
  article = get_object_or_404(Article, id = id)

  comments = article.comments.all()
  return render(request, "detail.html", {"article" : article, "comments" : comments})

@login_required(login_url="user:login")
def updateArticle(request, id):
  article = get_object_or_404(Article, id = id)
  form = ArticleFrom(request.POST or None, request.FILES or None, instance=article)
  if form.is_valid():
    article = form.save(commit = False)
    article.author = request.user
    article.save()
    messages.success(request, "Makale başarıyla güncellendi.")
    return redirect("../dashboard")
  else:    
    return render(request, "update.html", {"form" : form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
  article = get_object_or_404(Article, id = id)
  article.delete()
  messages.success(request, "Makale başarıyla silindi.")
  return redirect("article:dashboard")

@login_required(login_url="user:login")
def addComment(request, id):
  article = get_object_or_404(Article, id= id)
  if request.method == "POST":
    comment_author = request.POST.get("comment_author")
    comment_content = request.POST.get("comment_content")

    newComment = Comment(comment_author = comment_author, comment_content = comment_content)
    newComment.article = article
    newComment.save()
  
  return redirect(reverse("article:detail", kwargs={"id":id}))