import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Ex.: John27')
        add_placeholder(self.fields['email'], 'Ex.: John27@email.com')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')

    username = forms.CharField(
        label='Username',
        help_text='Required. Between 4 and 150 characters. Letters, digits and @/./+/-/_ only.',
        error_messages={'required': 'This field must not be empty',
                        'min_length': 'Username must have at least 4 characters',
                        'max_length': 'Username must have less than 150 characters'},
        min_length=4, max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Type your first name'},
        label='First Name',
        required=True
    )

    last_name = forms.CharField(
        error_messages={'required': 'Type your last name'},
        label='Last Name',
        required=True
    )

    email = forms.EmailField(
        error_messages={'required': 'Type your email'},
        label='E-mail',
        required=True
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat your Password',
        error_messages={'required': 'Please, repeat your password'},
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email)

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
