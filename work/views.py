from django.shortcuts import render, redirect
from django.core.mail import send_mail,send_mass_mail

# 导入验证码相关的包
from PIL import Image,ImageDraw,ImageFont
from django.contrib.auth import authenticate ,login
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from .my_util import *
from .models import MyUser
from django.core.cache import cache

# Create your views here.


import random
import io

def get_verify_img(req):
    # 画布背景颜色
    bg_color = get_random_color()
    # 实例化一个画布
    image = Image.new('RGB',(130, 70), bg_color)
    # 实例化一个画笔
    draw = ImageDraw.Draw(image,'RGB')
    # 字体路径
    font_path = '/home/tom/py1803/day07/static/fonts/ADOBEARABIC-BOLDITALIC.OTF'
    # 创建字体
    font = ImageFont.truetype(font_path,30)
    source = 'qwertyuiopasdfghjjjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

    # 保存每次随机出来的字符
    code_srt = ''
    for i in range(4):
        text_color = get_random_color()
        tmp_num = random.randrange(len(source))
        random_str = source[tmp_num]
        draw.text((10+30*i,20),random_str,text_color,font)
        code_srt += random_str
    req.session['code'] = code_srt

#    获取一个缓存区
    buf = io.BytesIO()
    image.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')


def my_register(req):
    if req.method=="GET":
        return render(req,'register.html')
    else:
        params = req.POST
        u_name = params.get('u_name')
        u_pwd = params.get('u_pwd')
        u_confirm_pwd = params.get('u_confirm_pwd')
        # 这个是用户输入的验证码
        u_code = params.get('code')
        u_phone = params.get('u_phone')
        u_email = params.get('u_email')
        # 需要获取系统生成的验证码
        server_code = req.session.get("code")
        if server_code.lower() != u_code.lower():
            return HttpResponse("输入验证码有误")
        if u_name and len(u_name) > 3 and u_pwd and len(u_pwd) > 3 and u_confirm_pwd and len(u_confirm_pwd) > 3 \
                and u_pwd == u_confirm_pwd and server_code.lower() == u_code.lower() \
                and u_phone and len(u_phone) > 3 and u_email and len(u_email) > 3:
            exist_flag = MyUser.objects.filter(username=u_name).exists()

            if exist_flag:
                return HttpResponse("用户已经被注册")
            else:
            #                 用户输入信息合法，创建用户表
                user = MyUser.objects.create_user(username=u_name,
                                              password=u_pwd,
                                              phone=u_phone,
                                              email=u_email,
                                              is_active = 0
                                              )
# -------------------发邮件-----------------------
            # 生成随机字符
            random_str = get_random_str()
            url = 'http://120.79.36.58:12345/d7work/email/' + random_str

            #         加载激活模板
            tmp = loader.get_template('active.html')
            # 渲染
            html_str = tmp.render({'url': url})

            # 准备邮件信息
            title = '阿里offer'
            msg = ''

            email_from = settings.DEFAULT_FROM_EMAIL
            reciever = [
                u_email
            ]
            send_mail(title, msg, email_from, reciever, html_message=html_str)

            cache.set(random_str, u_email, 120)



            return HttpResponse('ok')
        else:
            return HttpResponse("用户输入不合法")
# 登录
def my_login(req):
    if req.method == 'GET':
        return render(req,'login.html')
    else:
        params = req.POST
        u_name = params.get('u_name')
        u_pwd = params.get('u_pwd')
        u_code = params.get('code')
        server_code = req.session.get("code")
        if server_code.lower() != u_code.lower():
            return HttpResponse("输入验证码有误")
        user = authenticate(username=u_name, password=u_pwd)
        if user:
            return redirect('/d7work/index')
        else:
            return HttpResponse("用户输入不合法1")
# 主界面
def index(req):
    return render(req,'index.html')
# 激活
def active(req, random_str):
    res = cache.get(random_str)
    if res:
        # 通过邮箱找到用户
        # 给用户的状态字段做更新，从未激活态变成激活态



        return HttpResponse(res+'激活成功')
    else:
        return HttpResponse("验证链接无效")
