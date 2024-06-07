import os
from datetime import datetime
import calendar
from statistics import mean, median, mode, StatisticsError
from django.db.models import IntegerField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, ExpressionWrapper
from django.db.models.functions import ExtractYear
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import get_current_timezone, now
from django.views.generic.edit import CreateView
import matplotlib.pyplot as plt
import os
from translate import Translator
from movies.models import Movie, Genre
from movies_tickets.models import Ticket, Showtime
from .forms import CustomUserCreationForm, EmployeeCreationForm, ReviewForm
from main.models import *
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)


def get_quote():
    url = 'https://favqs.com/api/qotd'
    response = requests.get(url)
    quote_data = response.json()
    quote = quote_data['quote']['body']
    translator = Translator(to_lang="ru")
    translation = translator.translate(quote)
    return translation


def homeView(request):
    latest_news = news_item.objects.latest('id')
    quote = get_quote()
    return render(request, 'home.html', {'latest_news': latest_news, 'quote': quote})


def aboutView(request):
    all_about_company = about_company.objects.all()
    return render(request, 'about_company.html',
                  {'all_items': all_about_company})


def vacanciesView(request):
    return render(request, 'vacancies.html')


def reviewsView(request):
    return render(request, 'reviews.html')


def promo_couponsView(request):
    return render(request, 'promo_coupons.html')


def contactView(request):
    return render(request, 'contacts.html')


def faqView(request):
    all_faq = faq.objects.all()
    return render(request, 'faq.html',
                  {'all_items': all_faq})


def about_companyView(request):
    return render(request, 'about_company.html')


def contactsView(request):
    employees = Employee.objects.all().select_related('user__contact')
    return render(request, 'contacts.html', {'employees': employees})


def newsView(request):
    all_news = news_item.objects.all()
    return render(request, 'news.html',
                  {'all_items': all_news})


def privacy_policyView(request):
    return render(request, 'privacy_policy.html')


def promo_couponsView(request):
    all_promocodes = promo_coupon.objects.all()
    return render(request, 'promo_coupons.html',
                  {'all_items': all_promocodes})


def reviewsView(request):
    all_reviews = review.objects.all()
    return render(request, 'reviews.html',
                  {'all_items': all_reviews})


def vacanciesView(request):
    all_vacancies = vacancy.objects.all()
    return render(request, 'vacancies.html',
                  {'all_items': all_vacancies})


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class EmployeeSignUp(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup_employee.html'


def is_client(user):
    return user.is_authenticated and not user.is_staff and not user.is_superuser


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_client), name='dispatch')
class AddReview(LoginRequiredMixin, CreateView):
    model = review
    form_class = ReviewForm
    template_name = 'add_review.html'
    success_url = '/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'profile.html')
    elif not request.user.is_staff and not request.user.is_superuser:
        client = get_object_or_404(Client, user=request.user)
        tickets = Ticket.objects.filter(user=client)
        return render(request, 'client_profile.html', {'tickets': tickets})
    elif request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all()
        movies = Movie.objects.all()
        showtimes = Showtime.objects.all()
        movie_title = request.GET.get('movie')
        if movie_title:
            tickets = tickets.filter(showtime__movie__title=movie_title)
        showtime_id = request.GET.get('showtime')
        if showtime_id:
            tickets = tickets.filter(showtime__id=showtime_id)
        date = request.GET.get('date')
        if date:
            tickets = tickets.filter(purchase_time__date=date)
        total_sales = tickets.aggregate(total=models.Sum('price'))['total']
        return render(request, 'staff_profile.html', {'tickets': tickets, 'movies': movies,
                                                      'showtimes': showtimes, 'total_sales': total_sales})


def read(request):
    genres = Genre.objects.all()
    return render(request, "edit_genres.html", {'genres': genres})


def create(request):
    if request.method == "POST":
        genre = Genre()
        genre.name = request.POST.get("name")
        genre.description = request.POST.get("description")
        if genre.name == '' or genre.name is None or genre.name.isspace():
            logger.error("Genre name is empty.")
            return HttpResponseRedirect("/")
        if genre.description == '' or genre.description is None or genre.description.isspace():
            logger.error("Genre description is empty.")
            return HttpResponseRedirect("/")
        genre.save()
        logger.info(f"Genre '{genre.name}' created.")
    return HttpResponseRedirect("/")


def update(request, id):
    try:
        genre = Genre.objects.get(id=id)
        if request.method == "POST":
            genre.name = request.POST.get("name")
            genre.description = request.POST.get("description")
            if genre.name == '' or genre.name is None or genre.name.isspace():
                logger.error("Genre name is empty.")
                return HttpResponseRedirect("/")
            if genre.description == '' or genre.description is None or genre.description.isspace():
                logger.error("Genre description is empty.")
                return HttpResponseRedirect("/")
            genre.save()
            logger.info(f"Genre '{genre.name}' updated.")
            return HttpResponseRedirect("/")
        return render(request, "edit_genre.html", {"genre": genre})
    except Genre.DoesNotExist:
        logger.error(f"Genre with id {id} not found.")
        return HttpResponseNotFound("<h2>Genre not found</h2>")


def delete(request, id):
    try:
        genre = Genre.objects.get(id=id)
        genre.delete()
        logger.info(f"Genre '{genre.name}' deleted.")
        return HttpResponseRedirect("/")
    except Genre.DoesNotExist:
        logger.error(f"Genre with id {id} not found.")
        return HttpResponseNotFound("<h2>Genre not found</h2>")


def index(request):
    c = calendar.HTMLCalendar()
    d = datetime.today()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)

    tz = get_current_timezone()
    stored_date = datetime.now()
    desired_date = stored_date + tz.utcoffset(stored_date)
    timezone_name = desired_date.astimezone().tzinfo
    context = {'d': d, 'html_out': html_out, 'timezone': timezone_name, 'date': desired_date}
    return render(request, 'index.html', context)


def stats(request):
    popular_movie = Ticket.objects.values('showtime__movie__title').annotate(ticket_count=Count('id')).order_by(
        '-ticket_count').first()

    profitable_movie = Ticket.objects.values('showtime__movie__title').annotate(total_profit=Sum('price')).order_by(
        '-total_profit').first()
    current_year = now().year
    clients = Client.objects.select_related('user__contact').annotate(
        age=ExpressionWrapper(current_year - ExtractYear('user__contact__date_of_birth'), output_field=IntegerField()))
    ages = [client.age for client in clients]
    try:
        avg_age = round(mean(ages), 2)
    except StatisticsError:
        avg_age = 0

    try:
        median_age = median(ages)
    except StatisticsError:
        median_age = 0

    sales = [ticket.price for ticket in Ticket.objects.all()]

    try:
        avg_sales = round(mean(sales), 2)
    except StatisticsError:
        avg_sales = 0

    try:
        mode_sales = mode(sales)
    except StatisticsError:
        mode_sales = 0

    try:
        median_sales = median(sales)
    except StatisticsError:
        median_sales = 0

    context = {
        'popular_movie': popular_movie,
        'profitable_movie': profitable_movie,
        'avg_age': avg_age,
        'median_age': median_age,
        'avg_sales': avg_sales,
        'mode_sales': mode_sales,
        'median_sales': median_sales,
    }
    return render(request, 'stats.html', context)


def clients_and_purchases(request):
    clients = Client.objects.exclude(user__employee__isnull=False).order_by('user__username')
    clients_and_purchases = []
    for client in clients:
        total_purchases = Ticket.objects.filter(user=client).aggregate(total=Sum('price'))['total'] or 0
        total_purchases = round(total_purchases, 2)
        clients_and_purchases.append((client, total_purchases))
    return render(request, 'clients_and_purchases.html', {'clients_and_purchases': clients_and_purchases})


def get_sales_by_movie():
    sales_by_movie = Ticket.objects.values('showtime__movie__title').annotate(
        total_sales=Sum('price')).order_by('-total_sales')
    return sales_by_movie


def sales_distribution_chart():
    sales_data = get_sales_by_movie()
    movies = [sale['showtime__movie__title'] for sale in sales_data]
    total_sales = [sale['total_sales'] for sale in sales_data]

    plt.figure(figsize=(8, 6))
    plt.pie(total_sales, labels=movies, autopct='%1.1f%%')
    plt.title('Распределение продаж по фильмам')
    plt.axis('equal')
    save_path = os.path.join(settings.MEDIA_ROOT, 'sales_distribution_chart.png')
    plt.savefig(save_path)


def movies_and_sales(request):
    sales_data = Ticket.objects.values('showtime__movie__title').annotate(total=Sum('price'))
    movies_and_sales = []
    for data in sales_data:
        total_sales = data['total'] or 0
        total_sales = round(total_sales, 2)
        movies_and_sales.append((data['showtime__movie__title'], total_sales))
    sales_distribution_chart()
    image_path = os.path.join(settings.MEDIA_URL, 'sales_distribution_chart.png')
    return render(request, 'movies_and_sales.html', {'movies_and_sales': movies_and_sales,
                                                     'image_path': image_path})

