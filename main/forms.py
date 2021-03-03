from django import forms

from django.conf import settings

from .models import City, Client, Article, Comment, ClientEdited

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.validators import FileExtensionValidator, RegexValidator

class AboutForm(forms.ModelForm):
    name = forms.CharField(label="Имя", error_messages={'required': ''})
    last_name = forms.CharField(label="Фамилия", error_messages={'required': ''})
    birthday = forms.DateInput()
    
    city = forms.ModelChoiceField(queryset = City.objects.all(), label = "Город", empty_label = None, error_messages={'required': 'Выберите город'})
    
    avatar = forms.ImageField(label = 'Изображение', validators = [FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension': 'Этот формат не поддерживается.'}, required = False)
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{7,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label="Номер телефона", error_messages={'required': ''}, validators = [phone_regex],)
    
    class Meta:
        model = Client
        fields = ('name', 'last_name', 'birthday', 'city', 'avatar', 'phone',)
        widgets = {
            'birthday':  forms.DateInput(format='%d-%m-%Y'),
        }
        
        
        
RELS = (
    ("free", "Свободен"),
    ("married", "Женат/Замужем"),
)
        
        
class BioEditForm(forms.ModelForm):
    name = forms.CharField(label="Имя", error_messages={'required': ''})
    last_name = forms.CharField(label="Фамилия", error_messages={'required': ''})
    birthday = forms.DateInput()
    city = forms.ModelChoiceField(queryset = City.objects.all(), label = "Город", empty_label = None, error_messages={'required': 'Выберите город'})
    
    
    relationships = forms.ChoiceField(choices = RELS)
    
    avatar = forms.ImageField(label = 'Изображение', validators = [FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension': 'Этот формат не поддерживается.'}, required = False)
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{7,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(label="Номер телефона", error_messages={'required': ''}, validators = [phone_regex],)
    
    class Meta:
        model = ClientEdited
        fields = ('name', 'last_name', 'birthday', 'city', 'relationships', 'avatar', 'phone',)
        widgets = {
            'birthday':  forms.DateInput(format='%d-%m-%Y'),
        }
        

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label = 'Заголовок')
    text = forms.CharField(label = 'Текст', widget=forms.widgets.Textarea())
    picture = forms.ImageField(label = 'Изображение', validators = [FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension': 'Этот формат не поддерживается.'}, required = False)
    
    class Meta:
        model = Article
        fields = ('title', 'text', 'picture',)
        
        
class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label = '', widget=forms.widgets.Textarea())
    
    class Meta:
        model = Comment
        fields = ('comment_text',)
        
        
class ReplenishBalanceForm(forms.ModelForm):
    balance = forms.IntegerField(label = 'Сумма пополнения')
    
    class Meta:
        model = Client
        fields = ('balance',)
        
        
class CashingBalanceForm(forms.ModelForm):
    balance = forms.IntegerField(label = 'Сумма обналичивания')
    
    class Meta:
        model = Client
        fields = ('balance',)
        
        
class SendingBalanceByIinForm(forms.ModelForm):
    balance = forms.IntegerField(label = 'Сумма отправления')
    iin = forms.CharField(label = 'ИИН получателя')
    
    class Meta:
        model = Client
        fields = ('balance', 'iin',)
        
        
class SendingBalanceByNumberForm(forms.ModelForm):
    balance = forms.IntegerField(label = 'Сумма отправления')
    phone = forms.CharField(label = 'Номер получателя')
    
    class Meta:
        model = Client
        fields = ('balance', 'phone',)