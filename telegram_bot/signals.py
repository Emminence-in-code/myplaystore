from django.apps.config import AppConfig
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from bot.mail import mail_admin
from .models import UploadedApp


@receiver(post_save,sender=UploadedApp)
def handle_author_notifications(sender,instance:UploadedApp,created,*args, **kwargs):
    if created:
        # todo send email here
        mail_admin(reverse('admin:index'))
    pass