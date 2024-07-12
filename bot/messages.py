import requests
from telegram import Update

from bot.utils import getOwner
from telegram_bot.models import CustomUser

REPLY_URL = 'https://api.telegram.org/bot7335489186:AAGvytPLouKdRyPMkd-ew7Or-SJq73gumsI/sendMessage'
URL = 'https://myplaystore.pythonanywhere.app'


def handleStart(update:Update,msg):
    x =requests.post(REPLY_URL,json={
        'chat_id':update.effective_chat.id,
        'text':msg,
        'reply_markup':{
            'inline_keyboard':[
            [{'text':'Upload App','web_app':{'url':f'{URL}/form/'+update.effective_user.username}}]
        ]}
    })


def handleClear(update:Update,*args, **kwargs):
    x = CustomUser.objects.filter(username = update.effective_user.username)
    if x.exists():
        for user in x:
            user.delete()
    
    requests.post(REPLY_URL,json={
        'chat_id':update.effective_chat.id,
        'text':"Deleted All Userdata",
    })
    

def handleAffliate(update:Update,*args, **kwargs):
    requests.post(REPLY_URL,json={
        'chat_id':update.effective_chat.id,
        'text':'Start Earning now by partnering with us Today',
        'reply_markup':{
            'inline_keyboard':[
            [{'text':'Start Earning','web_app':{'url':f'https://ref.myplaystore.ng'}}],
 [{'text':'Market Place','web_app':{'url':f'https://ref.myplaystore.ng/store'}}]
        ]}
    })



def informOwner(message):
    owner = getOwner()
    requests.post(REPLY_URL,json={
        'chat_id':owner,
        'text':message,
        'reply_markup':{
            'inline_keyboard':[
            [{'text':'Check App','web_app':{'url':f'https://myplaystore.pythonanywhere.com/admin/telegram_bot/uploadedapp/'}}],
        ]}
    })