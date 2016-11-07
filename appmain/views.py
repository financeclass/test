# coding:utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    return HttpResponse(u"welcome!  欢迎光临!")


def home(request):
    channellist = ['电影', '音乐', '小说', '代码']
    linklist = [['1']]
    for aa in channellist:
        linklist.append([aa, Blog.objects.filter(channel=aa).filter(is_public=True).order_by('-id')[:5]])
    linklist.append(['other', Blog.objects.exclude(channel__in=channellist).filter(is_public=True).order_by('-id')[:5]])
    context = {'user': request.user,
               'list': linklist,
               }
    return render(request, 'appmain/home.html', context)


def detail(request):
    link =  get_object_or_404(Blog,id=request.GET.get('linkid', 0))
    if link.user!=request.user and link.is_public==False:
        return HttpResponse(u"无权限")
    return render(request, 'appmain/detail.html', locals())


def help(request):
    return render(request, 'appmain/help.html')


def links(request):
    channellist = ['电影', '音乐', '小说', '代码']
    if request.GET.get('channel', None) == 'other':
        context = {'linklist': Blog.objects.exclude(channel__in=channellist).filter(is_public=True).order_by('-id')}
    else:
        context = {
        'linklist': Blog.objects.filter(channel=request.GET.get('channel', None)).filter(is_public=True).order_by(
            '-id')}
    context['type'] = 'links'
    return render(request, 'appmain/links.html', context)


@login_required(login_url="/userlogin/")
def mylinks(request):
    context = {'linklist': Blog.objects.filter(user=request.user).order_by('-id'), 'type': 'mylinks'}
    return render(request, 'appmain/links.html', context)


@login_required(login_url="/userlogin/")
def mark(request):
    # TODO: 补全http
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            # TODO: 创建，收藏则获取id
            # 区别来自收藏
            if int(request.GET.get('edit', 0)) == 0:
                newblog=Blog.objects.create(title=form.cleaned_data['title'],
                                    channel=form.cleaned_data['channel'],
                                    content=form.cleaned_data['content'],
                                    url=form.cleaned_data['url'],
                                    is_public=form.cleaned_data['is_public'],
                                    user=request.user)
                # print(newblog) 设置id
            else:
                # 修改
                Blog.objects.filter(id=request.GET.get('linkid', 0),
                                    user=request.user).update(title=form.cleaned_data['title'],
                                                              channel=form.cleaned_data['channel'],
                                                              content=form.cleaned_data['content'],
                                                              is_public=form.cleaned_data['is_public'],
                                                              url=form.cleaned_data['url'])
        return HttpResponseRedirect("/mylinks/")
    elif int(request.GET.get('linkid', 0)) > 0:
        # 收藏，传递id
        thebolg = Blog.objects.get(id=request.GET.get('linkid', 0))
        form = BlogForm(instance=thebolg)
        return render(request, 'appmain/mark.html', {'user': request.user, 'form': form})
    else:
        return render(request, 'appmain/mark.html', {'user': request.user, 'form': BlogForm()})


@login_required(login_url="/userlogin/")
def delete(request):
    Blog.objects.filter(id=request.GET.get('linkid', None), user=request.user).delete()
    return HttpResponseRedirect("/mylinks/")




@login_required(login_url="/userlogin/")
def space(request):
    context = []
    return render(request, 'appmain/space.html', context)


################register###################

def register(request):
    if request.method == 'POST':
        User.objects.create(username=request.POST.get('username', None), is_staff=True)
        u = User.objects.get(username=request.POST.get('username', None))
        u.set_password(request.POST.get('password', None))
        u.save()
        login(request, authenticate(username=request.POST.get('username', None),
                                    password=request.POST.get('password', None)))
        return HttpResponseRedirect("/home/")
    else:
        context = {'userlist': User.objects.all()}
        return render(request, 'appmain/register.html', context)


def userlogin(request):
    if request.method == 'POST':
        auth = authenticate(username=request.POST.get('username', None),
                            password=request.POST.get('password', None))
        if auth is not None:
            login(request, auth)
            # login next 无效
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'appmain/login.html', {'error_msg': '用户不存在或密码错误'})
    else:
        return render(request, 'appmain/login.html')


def userlogout(request):
    logout(request)
    return HttpResponseRedirect("/home/")


