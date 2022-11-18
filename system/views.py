from django.shortcuts import render

# Create your views here.
from django.http import request, QueryDict
from django.shortcuts import render, HttpResponse
from django.contrib import auth
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import system.models
from loguru import logger
import os

if os.path.exists("log"):
    pass
else:
    os.mkdir("log")
    logger.info("log 文件夹不存在，已自动创建")

logger.add("log/{time}.log", rotation="1 day", encoding="utf-8")


# Create your views here.
@csrf_exempt
@logger.catch
def login(request: request):
    if request.method == "GET":
        return render(request, "system/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        result = {}
        if user:
            result["status"] = 200
            result["msg"] = "登入成功"
            auth.login(request, user)
            logger.info(f"用户 {username} 登入成功")
            return HttpResponse(json.dumps(result))
        else:
            result["status"] = 403
            result["msg"] = "账号或密码错误"
            logger.info(f"用户 {username} 登入失败，账号或密码错误")
            return HttpResponse(json.dumps(result))


@csrf_exempt
@login_required
@logger.catch
def logout(request: request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        logger.info(f"用户 {request.user.username} 登出成功")
        auth.logout(request)
        result = {
            "status": 200,
            "msg": "登出成功"
        }
        return HttpResponse(json.dumps(result))


@login_required
@logger.catch
def user(request):
    path = request.path
    if path == "/user/panel/":
        title = "仪表盘"
    elif path == "/user/my-bans/":
        title = "我的封禁"
    elif path == "/user/all-bans/":
        title = "全部封禁"
    elif path == "/user/add-ban/":
        title = "添加封禁"
    else:
        title = "你似乎来到了没有东西的海洋"

    return render(request, "system/user.html", {
        "username": request.user.username,
        "title": title
    })


@login_required
@logger.catch
def panel(request):
    return render(request, "system/panel.html")


@login_required
@logger.catch
def all_bans(request):
    bans = list(system.models.Ban.objects.all())
    return render(request, "system/all-bans.html", {
        "bans": bans
    })


@login_required
@logger.catch
def my_bans(request):
    bans = list(system.models.Ban.objects.filter(operator=request.user.username))
    return render(request, "system/my-bans.html", {
        "bans": bans
    })


@login_required
@logger.catch
def add_ban(request):
    return render(request, "system/add-ban.html")


@logger.catch
def copyright(request):
    return render(request, "system/copyright.html")


@login_required
@logger.catch
def get_info(request):
    logger.info(f"用户 {request.user.username} 获取了用户信息")
    return HttpResponse(json.dumps({
        "status": 200,
        "msg": "获取成功 ",
        "data": {
            "username": request.user.username,
            "email": request.user.email,
            "key": request.user.key,
            "date_joined": request.user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": request.user.last_login.strftime("%Y-%m-%d %H:%M:%S")
        }
    }))


@login_required
@csrf_exempt
@logger.catch
def change_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            auth.logout(request)
            logger.info(f"用户 {request.user.username} 修改密码成功")
            return HttpResponse(json.dumps({
                "status": 200,
                "msg": "修改成功"
            }))
        else:
            logger.info(f"用户 {request.user.username} 修改密码失败，旧密码错误")
            return HttpResponse(json.dumps({
                "status": 403,
                "msg": "原密码错误"
            }))
    else:
        return HttpResponse(json.dumps({
            "status": 403,
            "msg": "请求方式错误"
        }))


@csrf_exempt
@logger.catch
def blacklist(request):
    # 黑名单增删查改 API，遵循 REST 风格
    if request.method == "GET":
        # GEt 获取
        bl = list(system.models.Ban.objects.all().values())
        for i in range(len(bl)):
            bl[i]["time"] = bl[i]["time"].strftime("%Y-%m-%d %H:%M:%S")

        return HttpResponse(json.dumps({
            "status": 200,
            "msg": "获取成功",
            "data": bl
        }))
    elif request.method == "POST":
        # POSt 添加
        result = {}
        if request.user.is_authenticated:
            key = request.user.key
        else:
            try:
                key = request.POST["key"]
            except KeyError:
                result["status"] = 403
                result["msg"] = "缺少必要的参数：key, QQ, reason"
                return HttpResponse(json.dumps(result))
        try:
            QQ = request.POST["QQ"]
            reason = request.POST["reason"]
        except KeyError:
            result["status"] = 403
            result["msg"] = "缺少必要的参数：key, QQ, reason"
            return HttpResponse(json.dumps(result))

        try:
            user = system.models.User.objects.get(key=key)
        except system.models.User.DoesNotExist:
            result["status"] = 403
            result["msg"] = "无效的key"
            return HttpResponse(json.dumps(result))

        try:
            system.models.Ban.objects.get(QQ=QQ)
        except system.models.Ban.DoesNotExist:
            system.models.Ban.objects.create(operator=user.username, QQ=QQ, reason=reason)
            result["status"] = 200
            result["msg"] = "添加成功"
            logger.info(f"用户 {user.username} 添加了 {QQ} 到黑名单，原因：{reason}")
            return HttpResponse(json.dumps(result))

        result["status"] = 403
        result["msg"] = "已存在此封禁"
        logger.info(f"用户 {user.username} 试图添加 {QQ} 到黑名单，已存在此封禁")
        return HttpResponse(json.dumps(result))
    elif request.method == "DELETE":
        # DELETE 删除
        result = {}
        delete = QueryDict(request.body)
        if not request.user.is_authenticated:
            key = delete.get("key")
            if key is None:
                result["status"] = 403
                result["msg"] = "缺少必要参数：key，QQ"

                return HttpResponse(json.dumps(result))
        else:
            key = request.user.key

        qq = delete.get("QQ")
        if qq is None:
            result["status"] = 403
            result["msg"] = "缺少必要参数：key，QQ"

            return HttpResponse(json.dumps(result))
        try:
            user = system.models.User.objects.get(key=key)
        except system.models.User.DoesNotExist:
            result["status"] = 403
            result["msg"] = "无效的key"

            return HttpResponse(json.dumps(result))

        try:
            ban = system.models.Ban.objects.get(QQ=qq)
        except system.models.Ban.DoesNotExist:
            result["status"] = 403
            result["msg"] = "不存在此封禁"
            logger.info(f"用户 {user.username} 试图删除 {qq} 的封禁，不存在此封禁")
            return HttpResponse(json.dumps(result))

        if ban.operator == user.username:
            ban.delete()
            result["status"] = 200
            result["msg"] = "删除成功"
            logger.info(f"用户 {user.username} 删除了 {qq} 的封禁")
            return HttpResponse(json.dumps(result))
        else:
            result["status"] = 403
            result["msg"] = "此封禁不是你添加的"
            logger.info(f"用户 {user.username} 试图删除 {qq} 的封禁，此封禁不是你添加的")
            return HttpResponse(json.dumps(result))
