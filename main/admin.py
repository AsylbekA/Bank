from django.contrib import admin

from .models import City, Client, Article, Comment, ClientEdited, PaymentHistory

# Register your models here.

admin.site.register(City)
admin.site.register(Client)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ClientEdited)
admin.site.register(PaymentHistory)