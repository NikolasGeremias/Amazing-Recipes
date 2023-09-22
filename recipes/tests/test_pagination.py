from django.urls import reverse

from utils.pagination import make_pagination_range

from .test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa:E501
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)
        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_current(self):
        # Current page = 20 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_if_recipes_per_page_are_correct_in_home(self):
        for i in range(20):
            self.make_recipe(
                slug=f'recipe-{i}', author_data={'username': f'user{i}'}
            )

        response = self.client.get(reverse('recipes:home'))
        context = response.context['recipes']

        self.assertEqual(len(context), 9)

    def test_make_pagination_returns_first_page_when_page_equals_string(self):
        for i in range(10):
            self.make_recipe(
                slug=f'recipe-{i}', author_data={'username': f'user{i}'}
            )

        response = self.client.get(reverse('recipes:home') + '?page=anystring')
        context = response.context['pagination_range']

        self.assertEqual(context['current_page'], 1)
