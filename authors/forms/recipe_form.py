from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title', 'description', 'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit', 'preparation_steps', 'cover'
        )

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('People', 'People'),
                    ('Meals', 'Meals'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        prep_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(prep_time):
            self._my_errors['preparation_time'].append(
                'This field must be a positive number')

        return prep_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                'This field must be a positive number')

        return servings
