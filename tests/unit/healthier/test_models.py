"""
unit tests for Heathier app models
"""

from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from healthier.models import Brand, Category, Food_item, Store


class Food_item_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        food = Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit" +
            "/3103220009512/chamallows-haribo",
            name="Chamallows",
            nutri_score_fr="d",
            nova_grade=3,
            image_url="https://static.openfoodfacts.org/images/products" +
            "/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="1",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )
        Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit" +
            "/3103220009512/chamallows-haribo",
            name="Chamallows mallows",
            nutri_score_fr="a",
            nova_grade=2,
            image_url="https://static.openfoodfacts.org/images/products" +
            "/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="2",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )
        Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit" +
            "/3103220009512/chamallows-haribo",
            name="bananes",
            nutri_score_fr="c",
            nova_grade=3,
            image_url="https://static.openfoodfacts.org/images/products" +
            "/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="3",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )
        food4 = Food_item.objects.create(
            open_food_facts_url="https://fr.openfoodfacts.org/produit" +
            "/3103220009512/chamallows-haribo",
            name="saucisson",
            nutri_score_fr="c",
            nova_grade=3,
            image_url="https://static.openfoodfacts.org/images/products" +
            "/310/322/000/9512/front_fr.54.400.jpg",
            id_open_food_facts="4",
            energy_100g="326kcal",
            image_nutrition_url="326kcal",
        )

        user = User.objects.create_user(
            "lif65zefus@lkjlkj.eeg",
            email="lif65zefus@lkjlkj.eeg",
            password="123456789",
        )
        food.favoris.add(user)
        Category.objects.create(name="bonbons")
        Category.objects.create(name="chocolats")
        Category.objects.create(name="glaces")
        Category.objects.create(name="viandes")
        Category.objects.create(name="boissons")
        Category.objects.create(name="aliment sucré")
        Category.objects.create(name="aliment salé")
        cat = Category.objects.get(name="aliment salé")
        food4.categories.add(cat)

    def test_OFF_url_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field(
            "open_food_facts_url"
        ).verbose_name
        self.assertEquals(field_label, "open food facts url")

    def test_name_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_nutri_score_fr_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field("nutri_score_fr").verbose_name
        self.assertEquals(field_label, "nutri score fr")

    def test_nova_grade_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field("nova_grade").verbose_name
        self.assertEquals(field_label, "nova grade")

    def test_image_url_fr_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field("image_url").verbose_name
        self.assertEquals(field_label, "image url")

    def test_id_open_food_facts_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field(
            "id_open_food_facts"
        ).verbose_name
        self.assertEquals(field_label, "id open food facts")

    def test_energy_100g_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field("energy_100g").verbose_name
        self.assertEquals(field_label, "energy 100g")

    def test_image_nutrition_url_label(self):
        food_item = Food_item.objects.get(name="Chamallows")
        field_label = food_item._meta.get_field(
            "image_nutrition_url"
        ).verbose_name
        self.assertEquals(field_label, "image nutrition url")

    def test_str(self):
        food_item = Food_item.objects.get(name="Chamallows")
        self.assertEquals(food_item.__str__(), "Chamallows")

    def test_get_favorites(self):
        user = User.objects.get(username="lif65zefus@lkjlkj.eeg")
        food_item = Food_item.objects.get(name="Chamallows")
        favoris = list(Food_item.get_favorites(user.username))[0]
        self.assertEquals(favoris, food_item)
        food_item.favoris.all().delete()
        favoris = Food_item.get_favorites(user.username)
        self.assertEquals(favoris, False)

    def test_save_favorites(self):
        user = User.objects.get(username="lif65zefus@lkjlkj.eeg")
        food_item = Food_item.objects.get(name="Chamallows")
        self.assertEquals(
            Food_item.save_favorites(food_item.id, user),
            {"result": "already existing", "status": False},
        )
        food_item.favoris.remove(user)
        self.assertEquals(
            Food_item.save_favorites(food_item.id, user),
            {"result": "added", "status": True},
        )
        self.assertEquals(
            Food_item.save_favorites(10000, user),
            {"result": "unforeseen exception", "status": False},
        )

    def test_get_search(self):
        food_item = Food_item.objects.get(name="Chamallows mallows")
        f2 = (
            Food_item.objects.filter(name__icontains="mkjrdv")
            .order_by("name")
            .distinct("name")
        )
        self.assertEquals((food_item, 1), Food_item.search(food_item.name))
        results = Food_item.search("mkjrdv")
        self.assertEquals(results[1], 0)
        self.assertQuerysetEqual(results[0], f2)
        results = Food_item.search("Chamallows")
        self.assertEquals(results[1], 2)
        self.assertQuerysetEqual(
            results[0], ["Chamallows", "Chamallows mallows"], transform=str
        )

    def test_replace(self):
        food_names = [
            "Chamallows",
            "Chamallows mallows",
            "bananes",
            "saucisson",
        ]
        food_items = []
        {
            food_items.append(Food_item.objects.get(name=name))
            for name in food_names
        }
        categories_names = [
            "bonbons",
            "chocolats",
            "glaces",
            "viandes",
            "boissons",
            "aliment sucré",
        ]
        categories = {
            Category.objects.get(name=name) for name in categories_names
        }
        # no healthier food is returned for Chamallows
        self.assertEquals(Food_item.replace(food_items[0]), (False, None))
        {
            food_item.categories.add(category)
            for category in categories
            for food_item in food_items
        }
        # only "Chamallows mallows" is returned with better NOVA and
        # Nutri-score
        self.assertQuerysetEqual(
            Food_item.replace(food_items[0])[1],
            ["Chamallows mallows"],
            transform=str,
        )
        self.assertEquals(
            Food_item.replace(food_items[0])[0], True,
        )
        # ["bananes", "Chamallows mallows","saucisson"] are returned
        # with better Nutri-score only
        self.assertQuerysetEqual(
            Food_item.replace(food_items[0], status="nutri-only")[1],
            ["bananes", "Chamallows mallows", "saucisson"],
            transform=str,
            ordered=False,
        )

    def test_get_searched_food_Item(self):
        def mock_search_1(food_name):
            return food_name, 1

        def mock_search_2(food_name):
            return food_name, 2

        def mock_search_0(food_name):
            return food_name, 0

        def mock_replace_True(food_item, status=None):
            return True, "replacement_for " + food_item

        def mock_replace_False(food_item, status=None):
            return False, None

        # no item found for given name
        with mock.patch(
            "healthier.models.Food_item.search", new=mock_search_0
        ):
            self.assertEquals(
                Food_item.get_searched_food_Item(
                    food_name="name", food_id=None
                ),
                {
                    "status": "not_found",
                    "replacement_items": None,
                    "to_be_replaced_item": None,
                },
            )

        with mock.patch(
            "healthier.models.Food_item.search", new=mock_search_1
        ):
            # item found for given name and replacement item found
            with mock.patch(
                "healthier.models.Food_item.replace", new=mock_replace_True
            ):
                self.assertEquals(
                    Food_item.get_searched_food_Item(
                        food_name="name", food_id=None
                    ),
                    {
                        "status": "ok",
                        "replacement_items": "replacement_for name",
                        "to_be_replaced_item": "name",
                    },
                )
            # item found for given name and no replacement item found
            with mock.patch(
                "healthier.models.Food_item.replace", new=mock_replace_False
            ):
                self.assertEquals(
                    Food_item.get_searched_food_Item(
                        food_name="name", food_id=None
                    ),
                    {
                        "status": "no_replacement",
                        "replacement_items": None,
                        "to_be_replaced_item": "name",
                    },
                )
        # several items found for given name, user must make a choice
        with mock.patch(
            "healthier.models.Food_item.search", new=mock_search_2
        ):
            self.assertEquals(
                Food_item.get_searched_food_Item(
                    food_name="name", food_id=None
                ),
                {
                    "status": "choice_to_make",
                    "replacement_items": None,
                    "to_be_replaced_item": "name",
                },
            )


class Brand_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        Brand.objects.create(name="herta")

    def test_brand_name_label(self):
        brand = Brand.objects.get(name="herta")
        field_label = brand._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_str(self):
        brand = Brand.objects.get(name="herta")
        self.assertEquals(brand.__str__(), "herta")


class Category_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="boissons chocolatées")

    def test_category_name_label(self):
        category = Category.objects.get(name="boissons chocolatées")
        field_label = category._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_str(self):
        category = Category.objects.get(name="boissons chocolatées")
        self.assertEquals(category.__str__(), "boissons chocolatées")


class Store_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        Store.objects.create(name="Carrefour")

    def test_category_name_label(self):
        store = Store.objects.get(name="Carrefour")
        field_label = store._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_str(self):
        store = Store.objects.get(name="Carrefour")
        self.assertEquals(store.__str__(), "Carrefour")
