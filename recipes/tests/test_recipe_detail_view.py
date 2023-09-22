from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        needed_title = 'This is a detail test - It loads one recipe'

        # Create recipe
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={
                                               'id': 1
                                           }))
        content = response.content.decode('utf-8')

        # Check if one recipes exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_doesnt_load_recipe_not_published(self):

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        # Check if one recipes exists
        self.assertEqual(response.status_code, 404)
