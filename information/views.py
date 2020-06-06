from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
from information.models import User, Storage
from utils.common import paging


def login_check(func):
    """
    登录校验
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login')
        return func(request, *args, **kwargs)
    return wrapper


@login_check
def sindex(request):
    """
    学生页面
    :param request:
    :return:
    """
    return render(request, 'sindex.html')


@login_check
def tindex(request):
    """
    机构页面
    :param request:
    :return:
    """
    return render(request, 'tindex.html')


@login_check
def welcome(request):
    """
    欢迎页面
    :param request:
    :return:
    """
    user_id = request.session.get('user_id')
    user_info = User.objects.get(id=user_id)
    # 学生欢迎页面
    if user_info.type == 1:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        storage_count = Storage.objects.filter(user_id=user_id).count()
        approve_pass_count = Storage.objects.filter(user_id=user_id, state=1).count()
        data = {
            'time_now': time_now,
            'storage_count': storage_count,
            'approve_pass_count': approve_pass_count
        }
        return render(request, 'welcome_s.html', data)
    # 机构欢迎页面
    else:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        storage_count = Storage.objects.all().count()
        unapprove_count = Storage.objects.filter(state=0).count()
        data = {
            'time_now': time_now,
            'storage_count': storage_count,
            'unapprove_count': unapprove_count
        }
        return render(request, 'welcome_t.html', data)


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(number=username)
        if user:
            user_info = User.objects.get(number=username)
            if user_info.pwd == password:
                if user_info.type == 1:
                    request.session['number'] = user_info.number
                    request.session['user_id'] = user_info.id
                    data = {
                        'code': 0,
                        'msg': '登录成功！',
                        'url': '/sindex/'
                    }
                    return JsonResponse(data)
                elif user_info.type == 0:
                    request.session['number'] = user_info.number
                    request.session['user_id'] = user_info.id
                    data = {
                        'code': 0,
                        'msg': '登录成功！',
                        'url': '/tindex/'
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'code': -2,
                    'msg': '账户或密码错误！',
                }
                return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '用户不存！'
            }
            return JsonResponse(data)
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        number = request.POST.get('number')
        name = request.POST.get('name')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        phoneNumber = request.POST.get('phoneNumber')
        college = request.POST.get('college')
        major = request.POST.get('major')
        sclass = request.POST.get('sclass')
        if User.objects.filter(number=number):
            data = {
                'code': -1,
                'msg': '当前学号已注册！'
            }
            return JsonResponse(data)
        else:
            user_info = User()
            user_info.number = number
            user_info.name = name
            user_info.pwd = password
            user_info.sex = sex
            user_info.age = age
            user_info.phoneNumber = phoneNumber
            user_info.college = college
            user_info.major = major
            user_info.sclass = sclass
            user_info.save()
            print(request.POST)
            data = {
                'code': 0,
                'msg': '注册成功！'
            }
            return JsonResponse(data)
    else:
        return render(request, 'register.html')


@login_check
def updatepwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        user_id = request.POST.get('user_id')
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        renewpwd = request.POST.get('renewpwd')
        if newpwd == renewpwd:
            if user_id:
                user_info = User.objects.get(id=user_id)
                if user_info.pwd == oldpwd:
                    user_info.pwd = newpwd
                    user_info.save()
                    data = {
                        'code': 0,
                        'msg': '修改成功！',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'code': -1,
                        'msg': '旧密码错误！',
                    }
                    return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '两次输入新密码不一致！',
            }
            return JsonResponse(data)
    else:
        return render(request, 'updatepwd.html')

def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            del request.session['number']
            del request.session['user_id']
        except KeyError as e:
            print(e)
        return redirect('/login/')


@login_check
def all_user_page(request):
    """
    所以用户页面
    :param request:
    :return:
    """
    return render(request, 'all-user-page.html')


@login_check
def all_user(request):
    """
    所以学生 数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    number = request.GET.get('number')
    if number:
        obj = User.objects.filter(number__contains=number)
    else:
        obj = User.objects.all()
    # 调用公共方法
    info = paging(page, limit, obj)
    data = list()
    for user in info['objs']:
        user_dict = dict()
        user_dict['id'] = user.id
        user_dict['name'] = user.name
        user_dict['number'] = user.number
        user_dict['pwd'] = user.pwd
        user_dict['age'] = user.age
        user_dict['phoneNumber'] = user.phoneNumber
        user_dict['sex'] = user.sex
        data.append(user_dict)
    res = {
        "msg": "success",
        "code": "0",
        "count": info['objs_count'],
        "data": data
    }
    return JsonResponse(res)


@login_check
def add_storage(request):
    """
    学生添加存证
    :param request:
    :return:
    """
    if request.method == 'POST':
        print(request.POST)
        storage_text = request.POST.get('storage_text')
        storage_img = request.FILES.get('storage_img', None)
        user_id = request.session.get('user_id')
        user_info = User.objects.get(id=user_id)
        storage_info = Storage()
        if storage_text:
            storage_info.storage_text = storage_text
        else:
            storage_info.storage_text = ''
        if storage_img:
            storage_info.storage_img = storage_img
            storage_info.storage_img_name = storage_img.name
        else:
            storage_info.storage_img = ''
            storage_info.storage_img_name = ''
        storage_info.user_id = user_id
        storage_info.user_name = user_info.name
        storage_info.user_number = user_info.number
        storage_info.save()
        data = {
            'code': 0,
            'msg': '提交成功!',
        }
        return JsonResponse(data)
    else:
        return render(request, 'add_storage.html')


@login_check
def my_storage_page(request):
    """
    查看我的存证申请页面
    :param request:
    :return:
    """
    return render(request, 'my_storage.html')


@login_check
def my_storage(request):
    """
    我的存证数据组装
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    user_id = request.session.get('user_id')
    print(user_id)
    objs = Storage.objects.filter(user_id=user_id, state=1)
    info = paging(page, limit, objs)
    storage_list = list()
    for storage in info['objs']:
        storage_dict = dict()
        storage_dict['id'] = storage.id
        if storage.storage_img:
            storage_dict['storage_img'] = str(storage.storage_img)
            storage_dict['storage_img_name'] = storage.storage_img_name
        else:
            storage_dict['storage_img'] = ''
            storage_dict['storage_img_name'] = ''
        storage_dict['number'] = storage.user_number
        storage_dict['name'] = storage.user_name
        storage_dict['storage_text'] = storage.storage_text
        storage_list.append(storage_dict)
    res = {
        "msg": "success",
        "code": "0",
        "count": info['objs_count'],
        "data": storage_list
    }
    print(storage_list)
    return JsonResponse(res)


@login_check
def all_unapprove_storage_page(request):
    """
    所以未审批的存证页面
    :param request:
    :return:
    """
    return render(request, 'all_unapprove_storage.html')


@login_check
def all_storage_page(request):
    """
    所以存证页面
    :param request:
    :return:
    """
    return render(request, 'all_storage.html')


@login_check
def all_unapprove_storage(request):
    """
    所以未审核的存证
    :param request:
    :return:
    """
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    number = request.GET.get('number')
    if number:
        objs = Storage.objects.filter(state=0, user_number__contains=number)
    else:
        objs = Storage.objects.filter(state=0)
    info = paging(page, limit, objs)
    storage_list = list()
    for storage in info['objs']:
        storage_dict = dict()
        storage_dict['id'] = storage.id
        storage_dict['storage_text'] = storage.storage_text
        if storage.storage_img:
            storage_dict['storage_img'] = str(storage.storage_img)
            storage_dict['storage_img_name'] = storage.storage_img_name
        else:
            storage_dict['storage_img'] = ''
            storage_dict['storage_img_name'] = ''

        storage_dict['number'] = storage.user_number
        storage_dict['name'] = storage.user_name
        storage_list.append(storage_dict)
    res = {
        "msg": "success",
        "code": "0",
        "count": info['objs_count'],
        "data": storage_list
    }
    return JsonResponse(res)


@login_check
def all_storage(request):
    """
    所有存证
    :param request:
    :return:
    """
    print(request.GET)
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    number = request.GET.get('number')
    if number:
        objs = Storage.objects.filter(user_number__contains=number)
    else:
        objs = Storage.objects.all()
    info = paging(page, limit, objs)
    storage_list = list()
    for storage in info['objs']:
        storage_dict = dict()
        storage_dict['id'] = storage.id
        storage_dict['storage_text'] = storage.storage_text
        storage_dict['state'] = storage.state
        if storage.storage_img:
            storage_dict['storage_img'] = str(storage.storage_img)
            storage_dict['storage_img_name'] = storage.storage_img_name
        else:
            storage_dict['storage_img'] = ''
            storage_dict['storage_img_name'] = ''
        storage_dict['approve_time'] = storage.approve_time
        storage_dict['number'] = storage.user_number
        storage_dict['name'] = storage.user_name
        storage_list.append(storage_dict)
    res = {
        "msg": "success",
        "code": "0",
        "count": info['objs_count'],
        "data": storage_list
    }
    return JsonResponse(res)


@login_check
def update_s(request):
    """
    学生更新个人信息
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_info = User.objects.get(id=user_id)
        name = request.POST.get('name')
        age = request.POST.get('age')
        phoneNumber = request.POST.get('phoneNumber')
        college = request.POST.get('college')
        major = request.POST.get('major')
        sclass = request.POST.get('sclass')
        user_info.age = age
        user_info.phoneNumber = phoneNumber
        user_info.name = name
        user_info.college = college
        user_info.major = major
        user_info.sclass = sclass
        user_info.save()
        data = {
            'code': 0,
            'msg': '修改成功!',
        }
        return JsonResponse(data)
    else:
        user_id = request.GET.get('user_id')
        user_info = User.objects.get(id=user_id)
        return render(request, 'update_s.html', {'user_info': user_info})


@login_check
def personal_information(request):
    """
    个人信息页面
    :param request:
    :return:
    """
    user_id = request.GET.get('user_id')
    user_info = User.objects.get(id=user_id)
    return render(request, 'personal_information.html', {'user_info': user_info})


@login_check
def delete_user(request):
    """
    删除用户
    :param request:
    :return:
    """
    user_id = request.POST.get('user_id')
    user_info = User.objects.get(id=user_id)
    if user_info.type == 0:
        data = {
            'code': -1,
            'msg': '老师用户不能删除！'
        }
        return JsonResponse(data)
    else:
        user_info.delete()
        data = {
            'code': 0,
            'msg': '删除成功！'
        }
        return JsonResponse(data)


@login_check
def t_add_storage(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        user_id = request.POST.get('user_id')
        storage_text = request.POST.get('storage_text', None)
        storage_img = request.FILES.get('storage_img', None)
        user_info = User.objects.get(id=user_id)
        storage_info = Storage()
        storage_info.user_id = user_id
        if storage_text:
            storage_info.storage_text = storage_text
        else:
            storage_info.storage_text = ''
        if storage_img:
            storage_info.storage_img = storage_img
            storage_info.storage_img_name = storage_img.name
        else:
            storage_info.storage_img = ''
            storage_info.storage_img_name = ''
        storage_info.user_name =user_info.name
        storage_info.user_number =user_info.number
        storage_info.state = 1
        storage_info.save()
        data = {
            'code': 0,
            'msg': '提交成功！'
        }
        return JsonResponse(data)
    else:
        user_list = User.objects.filter(type=1)
        return render(request, 't_add_storage.html', {'user_list': user_list})


@login_check
def Approved(request):
    """
    审核存证
    :param request:
    :return:
    """
    print(request.POST)
    id = request.POST.get('id')
    start = request.POST.get('start')
    storage_info = Storage.objects.get(id=id)
    storage_info.state = start
    storage_info.approve_time = datetime.now()
    storage_info.save()
    data = {
        'code': 0,
        'msg': '审批成功！'
    }
    return JsonResponse(data)


@login_check
def search_by_number(request):
    """
    学生用户查询
    :param request:
    :return:
    """
    print(request.POST)
    number = request.POST.get('number', None)
    data_list = list()
    if number:
        user_list = User.objects.filter(number__contains=number, type=1)
        for user in user_list:
            data_dict = dict()
            data_dict['ID'] = user.id
            data_dict['number'] = user.number
            data_dict['name'] = user.name
            data_list.append(data_dict)
        data = {
            'code': 0,
            'data_list': data_list,
        }
        return JsonResponse(data)
    else:
        data = {
            'code': 0,
            'data_list': [],
        }
        return JsonResponse(data)
