import requests
from telegram import Update

from telegram_bot.models import CustomUser

REPLY_URL = 'https://api.telegram.org/bot7335489186:AAGvytPLouKdRyPMkd-ew7Or-SJq73gumsI/sendMessage'

def handleStart(update:Update,msg):
    x =requests.post(REPLY_URL,json={
        'chat_id':update.effective_chat.id,
        'text':msg,
        'reply_markup':{
            'inline_keyboard':[
            [{'text':'Upload App','web_app':{'url':'https://0a3d-197-210-55-102.ngrok-free.app/form/'+update.effective_user.username}}]
        ]}
    })


def handleClear(update:Update,*args, **kwargs):
    x = CustomUser.objects.filter(username = update.effective_user.username)
    if x.exists():
        for user in x:
            x.delete()
    
    requests.post(REPLY_URL,json={
        'chat_id':update.effective_chat.id,
        'text':"Deleted All Userdata",
    })
    
