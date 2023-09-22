from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipes exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_doesnt_load_recipes_not_published(self):

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))

        # Check if one recipes exists
        self.assertEqual(response.status_code, 404)
