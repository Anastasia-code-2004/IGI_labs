"""
URL configuration for Cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import path

from Cinema import settings
from main.views import *
from main.views import SignUp
from movies_tickets import views
from movies_tickets.views import scheduleView, bookingView
from movies.views import moviesView, movieDetailsView
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', homeView, name='home'),
    re_path(r'^vacancies/$', vacanciesView, name='vacancies'),
    re_path(r'^reviews/$', reviewsView, name='reviews'),
    re_path(r'^promo_coupons/$', promo_couponsView, name='promo_coupons'),
    re_path(r'^contacts/$', contactsView, name='contacts'),
    re_path(r'^news/$', newsView, name='news'),
    re_path(r'^privacy_policy/$', privacy_policyView, name='privacy_policy'),
    re_path(r'^faq/$', faqView, name='faq'),
    re_path(r'^about_company/$', aboutView, name='about_company'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^signup/$', SignUp.as_view(), name='signup'),
    re_path(r'^signup_employee/$', EmployeeSignUp.as_view(), name='signup_employee'),
    re_path(r'^add_review/$', AddReview.as_view(), name='add_review'),
    re_path(r'^movies/$', moviesView, name='movies'),
    re_path(r'^movies/(?P<movie_id>\d+)/$', movieDetailsView, name='movie_details'),
    re_path(r'^schedules/$', scheduleView, name='schedules'),
    re_path(r'^booking/(?P<showtime_id>\d+)/$', bookingView, name='booking'),
    re_path(r'^booking/(?P<showtime_id>\d+)/buy_ticket/$', views.buy_ticket, name='buy_ticket'),
    re_path(r'^profile/$', profile, name='profile'),
    re_path(r'^client_profile/$', profile, name='client_profile'),
    re_path(r'^staff_profile/$', profile, name='staff_profile'),

    re_path(r'^edit_genres/$', read, name='edit_genres'),
    re_path(r'^create_genre/$', create),
    re_path(r'^edit_genre/(?P<id>\d+)/$', update, name='edit_genre'),
    re_path(r'^delete_genre/(?P<id>\d+)/$', delete),

    re_path(r'^index/$', index, name='index'),
    re_path(r'^stats$', stats, name='stats'),
    re_path(r'^clients_and_purchases$', clients_and_purchases, name='clients_and_purchases'),
    re_path(r'^movies_and_sales$', movies_and_sales, name='movies_and_sales'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
