import json
from pathlib import Path

import requests
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler

from bot.command_routing import MY_ROUTES
from bot.mail import mail_user
from flat_tokens.models import Token
from telegram_bot.models import CustomUser

from .models import CustomUser, UploadedApp
from .utils import generate_token as generate

BASE_DIR = Path(__file__).resolve().parent.parent

bot = Bot(settings.TELEGRAM_BOT_TOKEN)

dispatcher = Application.builder().token(bot.token).concurrent_updates(True).read_timeout(4).write_timeout(3).build()


@api_view(['POST'])
def index(request):
    update = Update.de_json(request.data,bot=bot)
    if update.callback_query:
        # handle callback
        pass
    elif update.message and update.message.text:
        if update.message.text.startswith('/'):
            # handle command
            command = update.message.text
            if command == '/start':
                initialize(
                    update.effective_user.username,full_name=update.effective_user.name
                    )
                MY_ROUTES[command](
                    update,
                    "Welcome to MyPlaystore Bot"
                    )
            elif command == '/clear':
                MY_ROUTES['/clear'](update)
            
            # ! RUN OTHER COMMANDS
            else:
                try:
                    MY_ROUTES.get(command)(update)
                except:
                    # tell user an error occured
                    
                    pass
        else:
            # handle message
            pass
    return Response({'status': 'success'})


@api_view(['POST'])
def confirmEmail(request,username):
    post_data:dict= request.data
    user = CustomUser.objects.filter(username=username).first()
    if 'email' in post_data.keys():
        email = post_data.get('email')
        # * set user email
        user.email = email
        user.save()
        token = generate(
            username=username,
        )
        mail_user(
            reciever_name=username,
            token=token.token,
            email=user.email
        )
    return Response({'status': 'success'})


@api_view(['POST'])
def confirmToken(request,username):
    post_data:dict= request.data
    user = CustomUser.objects.filter(username=username).first()
    token = post_data.get('confirm_token')
    is_valid = Token.validate_user_token(user=user,token=token)
    if is_valid:
        # * remove any previous user instance with the email
        previous_instances = CustomUser.objects.filter(email = user.email)
        if previous_instances.__len__() > 1:
            for _user in previous_instances:
                if _user.username != username:
                    _user.delete()

        # handle token is valid
        user.confirmed_email=True
        user.save()
        return Response({'status':'token is valid'},200)
    else:
        # handle invalid token 
        return Response(status=400,data={'error':'Confirmation Code is invalid or expired'})

def sendMessage(chatId,message):
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Button 1", "callback_data": "1"}],
        ],
        "inline_keyboard":[
            [{"text": "Button 2", "callback_data": "2"}]

        ]
    }
    x = requests.post('https://api.telegram.org/bot7335489186:AAGvytPLouKdRyPMkd-ew7Or-SJq73gumsI/sendMessage',{"chat_id":chatId,"text":message,'reply_markup': json.dumps(inline_keyboard)})


def formView(request,username):
    user = CustomUser.objects.filter(username = username)
    if not user.exists():
        initialize(username,username)
    if(not user[0].confirmed_email):
        return redirect_to_auth(username=username)
    user = user.first()
    if request.method == 'POST':
        try:
            data= request.POST
            new_app_upload = UploadedApp.objects.create(
                user = user,
                full_name = data['full_name'],
                email = user.email,
                description = data['desc'],
                company_name = data['company_name'],
                app_name = data['app_name'],
                platform = data['platform'],
                category = data['category'],
                version = data['version'],
                estimated_size = data['estimated_size'],
                image1 = request.FILES.get('image1'),
                image2 = request.FILES.get('image2'),
                image3 = request.FILES.get('image3'),
                image4 = request.FILES.get('image4'),
                image5 = request.FILES.get('image5'),
                app = request.FILES['app'],

            )
            new_app_upload.save()
            return redirect('success-page')
        except:
            messages.error(request,'File Upload Failed')

    return render(request,'formpage.html',{'email':user.email})


def validateEmailView(request,username):
    return render(
        request,
        'confirm_email.html',
        {'username':username}
        )


def redirect_to_auth(username):
    return redirect('signin',username=username)


def successPage(request):
    return render(request,'success.html')


# !TELEGRAM FUNCTIONS

def initialize(username,full_name):
    if CustomUser.objects.filter(username=username).exists():
        return
    user = CustomUser.objects.create(
        username = username,
        full_name=full_name
    )
    user.save()
