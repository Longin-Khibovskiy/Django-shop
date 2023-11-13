from django import forms
from .models import Shoes, Supplier, Order, Pos_order, Chegue
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ShoesForm(forms.Form):
    brand = forms.CharField(
        max_length=50,
        min_length=2,
        strip=True,
        label='Бренд'
    )
    name = forms.CharField(
        max_length=50,
        min_length=2,
        strip=True,
        label='Модель')

    description = forms.CharField(
        max_length=150,
        min_length=2,
        strip=True,
        label='Описание обуви',
        initial='Описание',
        widget=forms.Textarea)
    price = forms.FloatField(
        min_value=1,
        # step_size=10,
        label='Цена обуви',
        initial=40)
    photo = forms.ImageField(
        label='Фотография обуви',
        required=False)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        # fields = '__all__'
        fields = ['title', 'agent_name', 'agent_firstname', 'agent_patronymic', 'exist']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'floatingInput',
                    'placeholder': 'Название'
                }
            ),
            'agent_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя'
                }
            ),
            'agent_firstname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия'
                }
            ),
            'agent_patronymic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество'
                }
            ),
            'exist': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Поле не должно начинаться с цифры')
        return title


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Login user',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    email = forms.CharField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Create a password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control',}),
        min_length=2,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control', },
        )
    )
    content = forms.CharField(
        label='Тело письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 11, },
        )
    )
