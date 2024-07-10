from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def mail_user(
        reciever_name,
        token,
        email
):

    context = {
    "receiver_name":reciever_name,
    "token":token
    }

    receiver_email = email
    template_name = "email.html"
    convert_to_html_content =  render_to_string(
    template_name=template_name,
    context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    x = send_mail(
    subject="MyPlayStore OTP Code",
    message=plain_message,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[receiver_email]  , # recipient_list is self explainatory
    html_message=convert_to_html_content,
    fail_silently=False    # Optional
    )



def mail_admin(
   url
):

 

    template_name = "admin_email.html"
    convert_to_html_content =  render_to_string(
    template_name=template_name,
    context={
        'url':url
    }
    )
    plain_message = strip_tags(convert_to_html_content)
    super_user = UserModel.objects.filter(is_superuser =True).first()
    x = send_mail(
    subject="A User just Uploaded an app",
    message=plain_message,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[
        # settings.EMAIL_HOST_USER,
        super_user.email]  , # recipient_list is self explainatory
    html_message=convert_to_html_content,
    fail_silently=False    # Optional
    )
