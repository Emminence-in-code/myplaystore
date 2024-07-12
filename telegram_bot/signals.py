from django.apps.config import AppConfig
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from bot.mail import mail_admin,confirm_app_uploaded_mail
from .models import UploadHistory, UploadedApp


@receiver(post_save,sender=UploadedApp)
def handle_author_notifications(sender,instance:UploadedApp,created,*args, **kwargs):
    if created:
        try:
        # todo send email here
            UploadHistory.objects.create(
                username = instance.user.username,
                email = instance.user.email,
                app_name = instance.app_name,

            ).save()
            mail_admin('https://myplaystore.pythonanywhere.com/admin/telegram_bot/uploadedapp')
            confirm_app_uploaded_mail(user=instance.user)

        except:
            pass
    pass