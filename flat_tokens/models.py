from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from telegram_bot.models import CustomUser

from .generate import generate_token

# Create your models here.
user_model = CustomUser

class Token(models.Model):
    token = models.CharField(max_length=10,blank = True,null = True)
    user = models.ForeignKey(user_model,on_delete=models.CASCADE)
    expiry = models.DateTimeField(blank = True,null = True)
    created_at = models.DateTimeField(auto_created=True,auto_now=True)


    @staticmethod
    def clear_expired_tokens():
        try:
            current_time = datetime.now()
            qs = Token.objects.all()
            for item in qs:
                if current_time >= item.expiry:
                    item.delete()
        except:
            ...
    
    @staticmethod
    def validate_user_token(user:user_model,token:str)->bool:
        """
        checks if token is valid
        """
        return Token.objects.filter(user=user,token=token).exists()

    
    def save(self, *args, **kwargs) -> None:
        # make sure user has an email address
        if not self.user.email:
            raise Exception('Error: users email cannot be null or /',self.user.email,'/')
        # delete past token instances that belong to this user
        
        old_tokens = Token.objects.filter(user = self.user)
        if old_tokens.exists():
            for token_instance in old_tokens:
                token_instance.delete()
                
        if not self.expiry:
            
            self.expiry = datetime.now()+timedelta(hours=1)
            self.token = generate_token(4)
            
        return super().save(*args, **kwargs)