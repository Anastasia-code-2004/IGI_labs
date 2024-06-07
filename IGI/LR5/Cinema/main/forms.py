from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date

from django.forms import ModelForm

from main.models import contact, review, Employee, Client


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_regex = r'^\+375(29|33|44|25|17)\d{3}\d{2}\d{2}$'
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year)))
    phone = forms.CharField(
        validators=[RegexValidator(phone_regex, 'Phone number must be '
                                                'in the format: +375 (29|33|44|25|17) XXX-XX-XX')])

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'date_of_birth')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        Client.objects.create(user=user)

        contact.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )

        return user


class EmployeeCreationForm(CustomUserCreationForm):
    job_description = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField()

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('job_description', 'photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        Employee.objects.create(
            user=user,
            job_description=self.cleaned_data['job_description'],
            photo=self.cleaned_data['photo'],
        )

        return user


class ReviewForm(ModelForm):
    class Meta:
        model = review
        fields = ['name', 'rating', 'text']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError('Оценка должна быть в диапазоне от 1 до 5.')
        return rating
