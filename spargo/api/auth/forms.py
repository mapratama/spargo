from dateutil import parser
from dateutil.relativedelta import relativedelta

from django import forms
from django.utils import timezone

from spargo.apps.users.models import User
from spargo.core.fields import MobileNumberField


class APIRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    name = forms.CharField(max_length=30)
    mobile_number = MobileNumberField()
    gender = forms.ChoiceField(choices=User.GENDER)
    birthday = forms.CharField()
    push_notification_key = forms.CharField(max_length=254, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if User.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("User with this mobile number already exists")
        return mobile_number

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        try:
            birthday = parser.parse(birthday).date()
        except ValueError:
            raise forms.ValidationError("%s is not right formatted" % birthday)

        if birthday > timezone.now().date() - relativedelta(years=12):
            raise forms.ValidationError("Minimum age is 12 years")

        if birthday.year < 1900:
            raise forms.ValidationError("Birthday can't registered")

        return birthday

    def clean_name(self):
        return self.cleaned_data['name'].title()

    def save(self, *args, **kwargs):
        user = User.objects.create(
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name'],
            mobile_number=self.cleaned_data['mobile_number'],
            birthday=self.cleaned_data['birthday'],
            gender=self.cleaned_data['gender'],
            push_notification_key=self.cleaned_data['push_notification_key'],
        )
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user
