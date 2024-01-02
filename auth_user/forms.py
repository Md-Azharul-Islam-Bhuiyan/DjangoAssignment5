from django import forms
from .constants import GENDER_TYPE
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserLibraryAccount, UserAddress 


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    profile_picture = forms.ImageField()
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'gender', 'profile_picture','street_address', 'city', 'postal_code', 'country']

    def save(self, commit=True):
        user = super().save(commit=False) # ami database a data save korbo na ekhn
        if commit == True:
            user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            profile_picture = self.cleaned_data.get('profile_picture')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user = user,
                postal_code = postal_code,
                city = city,
                country = country,
                street_address = street_address
            )

            UserLibraryAccount.objects.create(
                user = user,
                birth_date = birth_date,
                gender = gender,
                profile_picture = profile_picture,
                account_no = 10000+user.id
            )
        return user
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
             self.fields[field].widget.attrs.update({
                 'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                 )
             })