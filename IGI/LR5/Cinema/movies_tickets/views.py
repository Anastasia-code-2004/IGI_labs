import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from main.models import Client, promo_coupon
from movies.models import Genre
from .models import Schedule, Showtime, Ticket


def scheduleView(request):
    all_schedules = Schedule.objects.all().order_by('date')
    all_genres = Genre.objects.all()
    all_showtimes = Showtime.objects.all()

    price = request.GET.get('price')
    if price:
        all_showtimes = all_showtimes.filter(price__lte=price, schedule__isnull=False)

    genre = request.GET.get('genre')
    if genre:
        all_showtimes = all_showtimes.filter(movie__genres__name=genre, schedule__isnull=False)

    date = request.GET.get('date')
    if date:
        all_schedules = all_schedules.filter(date=date)
    movie_title = request.GET.get('movie')
    if movie_title:
        all_showtimes = all_showtimes.filter(movie__title__icontains=movie_title, schedule__isnull=False)

    return render(request, 'movie_showings/schedules.html', {'all_schedules': all_schedules,
                                                             'all_genres': all_genres,
                                                             'all_showtimes': all_showtimes})


def bookingView(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    return render(request, 'movie_showings/booking.html', {'showtime': showtime})


@login_required
def buy_ticket(request, showtime_id):
    if request.user.is_staff or request.user.is_superuser:
        logging.error('Staff and superusers cannot buy tickets.')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    showtime = get_object_or_404(Showtime, id=showtime_id)
    client = get_object_or_404(Client, user=request.user)
    ticket_price = showtime.price  # Use the showtime price as the initial ticket price
    if showtime.available_seats > 0:
        promo_code = request.POST.get('promo_code', None)
        if promo_code:
            try:
                coupon = promo_coupon.objects.get(code=promo_code)
                if coupon.is_active:
                    discount = coupon.discount_in_percents
                    ticket_price = showtime.price - showtime.price * discount / 100
                    messages.success(request, 'Промокод успешно применен.')
                else:
                    messages.error(request, 'Промокод не активен.')
            except promo_coupon.DoesNotExist:
                messages.error(request, 'Промокод не найден.')
        tz = get_current_timezone()
        stored_date = datetime.now()
        desired_date = stored_date + tz.utcoffset(stored_date)
        Ticket.objects.create(user=client, showtime=showtime, price=ticket_price, purchase_time=desired_date)
        showtime.available_seats -= 1
        showtime.save()
    return redirect('schedules')



