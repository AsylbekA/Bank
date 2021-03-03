from django.contrib import admin
from django.urls import path, include

from .views import index, registerview, confirm_registration, homepage, profile, balance_replenish, balance_cashing, balance_send_by_iin, balance_send_by_number, article_publish, article_detail, article_delete, comment_delete, changing_bio, moderating_bio_all, moderating_bio, moderating_bio_accept, moderating_bio_decline

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', LoginView.as_view(redirect_field_name='main:add', template_name="main/login_website.html"), name = 'login'),
    path('accounts/logout/', LogoutView.as_view(next_page='main:homepage', template_name = "logged_out_website.html"), name = 'logout'),
    path('register/', registerview, name = 'register'),
    path('confirm_registration/<int:cid>/', confirm_registration, name = 'confirm_registration'),
    path('moderating_changes/accept/<str:cid>/', moderating_bio_accept, name = 'moderating_bio_accept'),
    path('moderating_changes/decline/<str:cid>/', moderating_bio_decline, name = 'moderating_bio_decline'),
    path('moderating_changes/<int:cid>/', moderating_bio, name = 'moderating_bio'),
    path('moderating_changes/all/', moderating_bio_all, name = 'moderating_bio_all'),
    path('homepage/', homepage, name = 'homepage'),
    path('profile/changing_bio/<int:cid>/', changing_bio, name = 'changing_bio'),
    path('profile/<int:cid>/', profile, name = 'profile'),
    path('balance/send/by_iin/', balance_send_by_iin, name = 'balance_send_by_iin'),
    path('balance/send/by_number/', balance_send_by_number, name = 'balance_send_by_number'),
    path('balance/replenish/', balance_replenish, name = 'balance_replenish'),
    path('balance/cashing/', balance_cashing, name = 'balance_cashing'),
    path('article/detail/<int:pk>/', article_detail, name = 'article_detail'),
    path('article/delete/<int:pk>/', article_delete, name = 'article_delete'),
    path('article/publish/', article_publish, name = 'article_publish'),
    path('comment/delete/<int:pk>', comment_delete, name = 'comment_delete'),
]