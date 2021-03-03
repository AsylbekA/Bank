from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, UserManager

from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponseRedirect, Http404

from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm

from .models import City, Client, Article, Comment, ClientEdited, PaymentHistory

from .forms import AboutForm, ArticleForm, CommentForm, ReplenishBalanceForm, CashingBalanceForm, SendingBalanceByIinForm, SendingBalanceByNumberForm, BioEditForm

from django.core.mail import send_mail

from django.contrib import messages

import random

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            return HttpResponseRedirect(reverse('main:homepage', args = ()))
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def homepage(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            article = Article.objects.order_by('-published')
            context = {'article' : article}
            return render(request, 'main/homepage.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        article = Article.objects.order_by('-published')
        context = {'article' : article}
        return render(request, 'main/homepage.html', context)
    
    
def profile(request, cid):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            sender_iin_history = PaymentHistory.objects.filter(sender_id=request.user.id, sender_iin=request.user.client.iin)
            
            sender_phone_history = PaymentHistory.objects.filter(sender_id=request.user.id, sender_phone=request.user.client.phone)
            
            reciever_iin_history = PaymentHistory.objects.filter(reciever_id=request.user.id, reciever_iin=request.user.client.iin)
            
            reciever_phone_history = PaymentHistory.objects.filter(reciever_id=request.user.id, reciever_phone=request.user.client.phone)
            
            context = {'sender_iin_history' : sender_iin_history, 'reciever_iin_history' : reciever_iin_history, 'sender_phone_history' : sender_phone_history, 'reciever_phone_history' : reciever_phone_history}
            return render(request, 'main/profile.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
        
def balance_replenish(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.method == 'POST':
                bal = ReplenishBalanceForm(request.POST)
                if bal.is_valid:
                    bal = bal.save(commit=False)
                    if bal.balance < 0:
                        bal = ReplenishBalanceForm()
                        error = True
                        context = {'form' : bal, 'error' : error}
                        return render(request, 'main/balance_replenish.html', context)
                    else:
                        request.user.client.balance += bal.balance
                        request.user.client.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
                else:
                    context = {'form' : bal}
                    return render(request, 'main/balance_replenish.html', context)
            else:
                bal = ReplenishBalanceForm()
                context = {'form' : bal}
                return render(request, 'main/balance_replenish.html', context)
        
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def balance_cashing(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.method == 'POST':
                bal = CashingBalanceForm(request.POST)
                if bal.is_valid:
                    bal = bal.save(commit=False)
                    if request.user.client.balance < bal.balance or bal.balance < 0:
                        bal = CashingBalanceForm()
                        error = True
                        context = {'form' : bal, 'error' : error}
                        return render(request, 'main/balance_cashing.html', context)
                    else:
                        request.user.client.balance -= bal.balance
                        request.user.client.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
                else:
                    context = {'form' : bal}
                    return render(request, 'main/balance_cashing.html', context)
            else:
                bal = CashingBalanceForm()
                context = {'form' : bal}
                return render(request, 'main/balance_cashing.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def balance_send_by_iin(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.method == 'POST':
                bal = SendingBalanceByIinForm(request.POST)
                if bal.is_valid:
                    bal = bal.save(commit=False)
                    reciever = Client.objects.get(iin=bal.iin)
                    if request.user.client.balance < bal.balance or bal.balance < 0:
                        bal = SendingBalanceByIinForm()
                        error = True
                        context = {'form' : bal, 'error' : error, 'reciever' : reciever}
                        return render(request, 'main/balance_sending.html', context)
                    else:
                        request.user.client.balance -= bal.balance
                        reciever.balance += bal.balance
                        PaymentHistory.objects.create(sender=request.user.client.name, reciever = reciever.name, amount=bal.balance, sender_id=request.user.id, reciever_id=reciever.clientid, reciever_iin=reciever.iin, sender_iin=request.user.client.iin)
                        reciever.save()
                        request.user.client.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
                else:
                    context = {'form' : bal}
                    return render(request, 'main/balance_sending.html', context)
            else:
                bal = SendingBalanceByIinForm()
                context = {'form' : bal}
                return render(request, 'main/balance_sending.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def balance_send_by_number(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.method == 'POST':
                bal = SendingBalanceByNumberForm(request.POST)
                if bal.is_valid:
                    bal = bal.save(commit=False)
                    reciever = Client.objects.get(phone=bal.phone)
                    if request.user.client.balance < bal.balance or bal.balance < 0:
                        bal = SendingBalanceByNumberForm()
                        error = True
                        context = {'form' : bal, 'error' : error, 'reciever' : reciever}
                        return render(request, 'main/balance_sending.html', context)
                    else:
                        request.user.client.balance -= bal.balance
                        reciever.balance += bal.balance
                        PaymentHistory.objects.create(sender=request.user.client.name, reciever = reciever.name, amount=bal.balance, sender_id=request.user.id, reciever_id=reciever.clientid, reciever_phone=reciever.phone, sender_phone=request.user.client.phone)
                        reciever.save()
                        request.user.client.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
                else:
                    context = {'form' : bal}
                    return render(request, 'main/balance_sending.html', context)
            else:
                bal = SendingBalanceByNumberForm()
                context = {'form' : bal}
                return render(request, 'main/balance_sending.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))

    
def article_detail(request, pk):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            article = get_object_or_404(Article, id=pk)
            comment = Comment.objects.filter(publicationcomment = pk)
            comment_id = get_object_or_404(Article, id = article.pk)
            if request.method == 'POST':
                cmn = CommentForm(request.POST)
                if cmn.is_valid():
                    cmn = cmn.save(commit=False)
                    cmn.comment_author = request.user.username
                    cmn.publicationcomment = comment_id
                    cmn.comment_authorid = request.user.id
                    cmn.save()
                    return HttpResponseRedirect(reverse('main:article_detail', args=(pk,)))
                else:
                    context = {'article' : article, 'comment' : comment, 'form' : cmn}
                    return render(request, 'main/article_detail.html', context)
            else:
                cmn = CommentForm()
                context = {'article' : article, 'comment' : comment, 'form' : cmn}
                return render(request, 'main/article_detail.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
        
#Исправить if status
        
def comment_delete(request, pk):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            comment = get_object_or_404(Comment, id=pk)
            if request.user.client.status == 'Moderator' or request.user.client.status == 'Admin':
                comment = get_object_or_404(Comment, id=pk)
                comment.delete()
                return HttpResponseRedirect(reverse('main:article_detail', args=(comment.publicationcomment.id,)))
            elif request.user.username == comment.comment_author:
                comment = get_object_or_404(Comment, id=pk)
                comment.delete()
                return HttpResponseRedirect(reverse('main:article_detail', args=(comment.publicationcomment.id,)))
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
        
    
def article_publish(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Moderator' or request.user.client.status == 'Admin':
                if request.method == 'POST':
                    art = ArticleForm(request.POST, request.FILES)
                    if art.is_valid():
                        art = art.save(commit=False)
                        art.author = request.user.username
                        art.save()
                        return HttpResponseRedirect(reverse('main:homepage', args = ()))
                    else:
                        context = {'form' : art}
                        return render(request, 'main/article_publish.html')
                else:
                    art = ArticleForm()
                    context = {'form' : art}
                    return render(request, 'main/article_publish.html', context)
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def article_delete(request, pk):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Moderator' or request.user.client.status == 'Admin':
                article = get_object_or_404(Article, id=pk)
                article.picture.delete()
                article.delete()
                return HttpResponseRedirect(reverse('main:homepage', args = ()))
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def registerview(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index', args=()))
    else:
        form = UserCreationForm()
        
    return render(request, 'main/register.html', {'form' : form})


def confirm_registration(request, cid):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cl = get_object_or_404(User, id = cid)
            af = AboutForm(request.POST, request.FILES)
            if af.is_valid():
                af = af.save(commit=False)
                
                cl.client.iin = str(random.randint(100000000000, 999999999999))
                users_iins = Client.objects.all()
                for users_iins in users_iins:
                    while users_iins.iin == cl.client.iin:
                        cl.client.iin = str(random.randint(100000000000, 999999999999))
                        
                cl.client.is_moderated = True
                cl.client.name = af.name
                cl.client.last_name = af.last_name
                cl.client.birthday = af.birthday
                cl.client.city = af.city
                cl.client.phone = af.phone
                cl.client.clientid = request.user.id
                cl.save()
                return HttpResponseRedirect(reverse('main:index', args=()))
            else:
                context = {'form' : af}
                return render(request, 'main/confirm_registration.html', context)
        else:
            af = AboutForm()
            context = {'form' : af}
            return render(request, 'main/confirm_registration.html', context)
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def changing_bio(request, cid):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.method == 'POST':
                bf = BioEditForm(request.POST, request.FILES)
                if bf.is_valid():
                    try:
                        client_edit = get_object_or_404(ClientEdited, clientid=cid)
                        bf = bf.save(commit=False)
                        client_edit.name = bf.name
                        client_edit.last_name = bf.last_name
                        client_edit.city = bf.city
                        client_edit.birthday = bf.birthday
                        client_edit.relationships = bf.birthday
                        client_edit.avatar = bf.avatar
                        client_edit.phone = bf.phone
                        client_edit.clientid = request.user.id
                        client_edit.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
                    except Http404:
                        bf = bf.save(commit=False)
                        bf.clientid = request.user.id
                        bf.save()
                        return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))  
                else:
                    context = {'form' : bf}
                    return render(request, 'main/changing_bio.html', context)
            else:
                bf = BioEditForm()
                context = {'form' : bf}
                return render(request, 'main/changing_bio.html', context)
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def moderating_bio_all(request):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Admin':
                clients = ClientEdited.objects.filter(changes_is_moderated=False)
                context = {'clients' : clients}
                return render(request, 'main/moderating_bio_all.html', context)
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def moderating_bio(request, cid):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Admin':
                client = ClientEdited.objects.order_by('-published').first()
                context = {'client' : client}
                return render(request, 'main/moderating_bio.html', context)
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def moderating_bio_accept(request, cid):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Admin':
                client_edited = get_object_or_404(ClientEdited, clientid=cid)
                client = get_object_or_404(User, id=cid)
                client.client.name = client_edited.name
                client.client.last_name = client_edited.last_name
                client.client.birthday = client_edited.birthday
                client.client.city = client_edited.city
                client.client.avatar = client_edited.avatar
                client.client.phone = client_edited.phone
                client.client.relationships = client_edited.relationships
                client_edited.delete()
                client.client.save()
                
                return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))
    
    
def moderating_bio_decline(request, cid):
    if request.user.is_authenticated:
        if request.user.client.is_moderated == True:
            if request.user.client.status == 'Admin':
                client_edited = get_object_or_404(ClientEdited, clientid=cid)
                client_edited.delete()
                return HttpResponseRedirect(reverse('main:profile', args = (request.user.id,)))
            else:
                return render(request, 'main/no_rights.html')
        else:
            return HttpResponseRedirect(reverse('main:confirm_registration', args=(request.user.id,)))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))