from django.db import models

from django.conf import settings

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True)
    city = models.TextField()
    avatar = models.ImageField(verbose_name = 'Фото профиля', null = True, blank = True)
    relationships = models.CharField(max_length = 30, default='Не указано')
    status = models.CharField(max_length = 30, default='Client')
    iin = models.CharField(default='x', max_length=12)
    clientid = models.TextField(default = 'Z')
    balance = models.IntegerField(default=0)
    is_moderated = models.BooleanField(default=False)
    changes_is_moderated = models.BooleanField(default=False)
    phone = models.CharField(default = 'z', max_length=11, validators=[MinLengthValidator(11)])
    
    def __str__(self):
        return self.name
    
    
class ClientEdited(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True)
    city = models.TextField()
    avatar = models.ImageField(verbose_name = 'Фото профиля', null = True, blank = True)
    relationships = models.CharField(max_length = 30, default='Не указано')
    status = models.CharField(max_length = 30, default='Client')
    clientid = models.TextField(default = 'Z')
    phone = models.CharField(default = 'z', max_length=11, validators=[MinLengthValidator(11)])
   
    changes_is_moderated = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add = True, db_index = True)
    
    def __str__(self):
        return self.name
    
    
class City(models.Model):
    cityname = models.CharField(max_length = 100, db_index = True)
    
    def __str__(self):
        return self.cityname
    
    
class PaymentHistory(models.Model):
    sender = models.CharField(max_length = 30, db_index = True)
    reciever = models.CharField(max_length = 30, db_index = True)
    sender_id = models.CharField(max_length = 30, db_index = True)
    reciever_id = models.CharField(max_length =30, db_index = True)
    sender_iin = models.CharField(max_length=30, db_index = True)
    sender_phone = models.CharField(max_length=30, db_index = True)
    reciever_iin = models.CharField(max_length=30, db_index = True)
    reciever_phone = models.CharField(max_length=30, db_index = True)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add = True, db_index = True)
    
    def __str__(self):
        return self.sender
    
class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=3000)
    picture = models.ImageField(verbose_name = 'Изображение', null = True, blank = True)
    author = models.CharField(max_length=50)
    published = models.DateTimeField(auto_now_add = True, db_index = True)
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    comment_text = models.CharField(max_length = 150)
    comment_author = models.CharField(max_length = 30, default = 'User')
    comment_authorid = models.TextField(default = 'z')
    comment_published = models.DateTimeField(auto_now_add = True, db_index = True)
    publicationcomment = models.ForeignKey('Article', null = True, blank = True, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.comment_text
    
    
@receiver(post_save, sender=User)
def create_user_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_client(sender, instance, **kwargs):
    instance.client.save()