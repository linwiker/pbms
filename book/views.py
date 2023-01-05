import json

from django.shortcuts import render, redirect, HttpResponse
from book import models


# Create your views here.

def index(request):
    """
    首页视图函数,查询所有的出版社,书籍,作者信息
    :param request:
    :return:出版社,书籍,作者信息
    """
    page_num = request.GET.get('page_num')
    if not page_num:
        page_num = 1
    all_book = models.Book.objects.all()
    all_publisher = models.Publisher.objects.all()
    all_author = models.Author.objects.all()
    return render(request, 'index.html',
                  {"all_publisher": all_publisher, 'all_book': all_book, 'all_author': all_author,
                   'page_num': page_num})


def add_publisher(request):
    """
    添加出版社视图函数
    :param request:
    :return:重定向回首页
    """
    if request.method == "POST":
        publisher_name = request.POST.get('publisher_name')
        publisher_addr = request.POST.get('publisher_addr')
        models.Publisher.objects.create(name=publisher_name,addr=publisher_addr)
        return redirect('/')


def add_book(request):
    """
    添加书籍视图函数
    :param request:
    :return:重定向回书籍管理页面
    """
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.getlist('author')
        publisher = request.POST.get('publisher')
        new_book_obj = models.Book.objects.create(title=title, publisher_id=publisher)
        new_book_obj.author.set(author)
        return redirect('/?page_num=2')


def add_author(request):
    """
    添加作者视图函数
    :param request:
    :return: 重定向回作者管理页面
    """
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        author_sex = request.POST.get('author_sex')
        author_age = request.POST.get('author_age')
        author_tel = request.POST.get('author_tel')
        models.Author.objects.create(name=author_name,sex=author_sex,age=author_age,tel=author_tel)
        return redirect('/?page_num=3')


def update_publisher(request):
    """
    更新出版社信息视图函数
    :param request:
    :return: 重定向回出版社管理页面
    """
    if request.method == "POST":
        publisher_id = request.POST.get('id')
        old_publisher = models.Publisher.objects.get(id=publisher_id)
        name = request.POST.get('publisher_name')
        addr = request.POST.get('publisher_addr')
        old_publisher.name = name
        old_publisher.addr = addr
        old_publisher.save()
        return redirect('/')


def update_book(request):
    """
        更新书籍信息视图函数
        :param request:
        :return: 重定向回书籍管理页面
        """
    if request.method == 'POST':
        book_id = request.POST.get('id')
        title = request.POST.get('title')
        author_list = request.POST.getlist('author')
        publisher = request.POST.get('publisher')
        old_book = models.Book.objects.get(id=book_id)
        old_author = models.Author.objects.filter(id__in=author_list)
        old_book.title = title
        old_book.publisher_id = publisher
        old_book.author.set(old_author)
        old_book.save()
        return redirect('/?page_num=2')


def update_author(request):
    """
        更新作者信息视图函数
        :param request:
        :return: 重定向回作者管理页面
        """
    if request.method == 'POST':
        author_id = request.POST.get('id')
        author_name = request.POST.get('author_name')
        author_sex = request.POST.get('author_sex')
        author_age = request.POST.get('author_age')
        author_tel = request.POST.get('author_tel')
        old_author = models.Author.objects.get(id=author_id)
        old_author.name = author_name
        old_author.sex = author_sex
        old_author.age = author_age
        old_author.tel = author_tel
        old_author.save()
        return redirect('/?page_num=3')


def delete_publisher(request):
    """
    删除出版社视图函数
    在删除出版社时,前端模态框通过ajax post请求返回出版社下包含的书籍信息.提示是否要删除其依赖
    :param request:
    :return:重定向回出版社管理页面
    """
    if request.method == "GET":
        publisher_id = request.GET.get('id')
        models.Publisher.objects.get(id=publisher_id).delete()
        return redirect('/')
    elif request.method == "POST":
        publisher_id = request.POST.get('id')
        book_obj = models.Book.objects.all().filter(publisher_id=publisher_id)
        title_list = []
        for book in book_obj:
            title_list.append(book.title)
        return HttpResponse(json.dumps(title_list), content_type="application/json")


def delete_book(request):
    """
    删除书籍视图函数
    :param request:
    :return: 重定向回书籍管理页面
    """
    book_id = request.GET.get('id')
    models.Book.objects.get(id=book_id).delete()
    return redirect('/?page_num=2')


def delete_author(request):
    """
    删除作者视图函数
    在删除作者时,前端模态框通过ajax post请求返回作者包含的书籍信息.提示是否要删除其依赖
    :param request:
    :return:重定向回作者管理页面
    """
    if request.method == "GET":
        author_id = request.GET.get('id')
        models.Author.objects.get(id=author_id).delete()
        return redirect('/?page_num=3')
    elif request.method == "POST":
        author_id = request.POST.get('id')
        book_obj = models.Book.objects.all().filter(author=author_id)
        title_list = []
        for book in book_obj:
            title_list.append(book.title)
        return HttpResponse(json.dumps(title_list), content_type="application/json")
