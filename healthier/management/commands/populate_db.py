"""
Script to populate healthier app Data Base with data from fr.OpenFoodFact API
use : manage.py populate_db <categories> or "all" with the argument "all"
the script will proceed to the extensive download of 100 food items from
all categories...
"""

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from ...models import Brand, Category, Food_item, Store


class Command(BaseCommand):
    help = "IMPORT DATA FROM OpenFoodFacts given a category list or 'all'"

    def add_arguments(self, parser):
        parser.add_argument("categories", nargs="+", type=str)

    def handle(self, *args, **options):
        try:
            if "all" in options:
                self.populate_with()
            else:
                for categorie in options["categories"]:
                    self.populate_with(categorie)
        except BaseException:
            pass

    def populate_with(self, categorie=all):
        if categorie == "all":
            # download the list of all categories from OFF API
            request = requests.get(
                "https://fr.openfoodfacts.org/categories.json")
            if request.status_code == 200:
                categories = {item["url"] for item in request.json()["tags"]}
                self.stdout.write("categories downloaded")
                categories = self.parse(categories)
                # download the food items from OFF API that have nutriscore and
                # novagrade and required fields
                for categorie in categories:
                    food_items = self.get_fooditems(categorie)
                    self.populate_db(food_items)
                    self.stdout.write(
                        "food items for category {} reviewed".format(categorie)
                    )
            else:
                self.stdout.write(
                    "unable to download categories (other than status 200...)"
                )

        else:
            # download the food items of the categorie from OFF
            food_items = self.get_fooditems(categorie)
            self.stdout.write(str(len(food_items)) + " food items downloaded")
            self.populate_db(food_items)

    def get_fooditems(
        self,
        categorie,
        number=50,
        fields=[
            "url",
            "product_name",
            "categories",
            "image_url",
            "nutriments",
            "nutrition_grade_fr",
            "nova_group",
            "id",
            "brands",
            "stores",
            "image_nutrition_url",
        ],
    ):
        self.stdout.write(
            "beginning downloading items for category {}".format(categorie)
        )
        request = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl",
            params={
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": categorie,
                "json": "true",
                "fields": ",".join(fields),
                "page_size": str(number) + "#" + str(number),
            },
        )
        if request.status_code == 200:
            food_items = []
            # sanity check...for values in required fields
            for product in request.json()["products"]:
                if (
                    product.get("nutrition_grade_fr")
                    and product.get("image_url")
                    and product["nutriments"].get("energy-kcal_100g")
                    and product.get("nova_group")
                    and product.get("product_name")
                    and product.get("id")
                    and product.get("stores")
                    and product.get("brands")
                    and product.get("categories")
                    and product.get("image_nutrition_url")
                ):
                    food_items.append(product)
            return food_items
        else:
            raise CommandError(
                "unable to download fooditems for "
                "category {}\n".format(categorie))

    def parse(self, list_of_url):
        # removes / from urls and non French names ("language : xxx" as
        # formated by OpenFoodFacts)
        parsed_urls = []
        {parsed_urls.append(url.split("/")) for url in list_of_url}
        categories = {
            parsed_url[-1] for parsed_url in parsed_urls if ":"
            not in parsed_url[-1]
        }
        return categories

    def populate_db(self, food_items):
        i = 0
        for food_item in food_items:
            try:
                new_food_item, created = Food_item.objects.get_or_create(
                    open_food_facts_url=food_item["url"],
                    name=food_item["product_name"],
                    energy_100g=str(food_item["nutriments"]["energy_value"])
                    + food_item["nutriments"]["energy_unit"],
                    nutri_score_fr=food_item["nutrition_grade_fr"],
                    nova_grade=food_item["nova_group"],
                    image_url=food_item["image_url"],
                    id_open_food_facts=food_item["id"],
                    image_nutrition_url=food_item["image_nutrition_url"],
                )
                if created:
                    i += 1
                    for category in food_item["categories"].split(","):
                        c, created = Category.objects.get_or_create(
                            name=category)
                        new_food_item.categories.add(c)
                    for store in food_item["stores"].split(","):
                        c, created = Store.objects.get_or_create(name=store)
                        new_food_item.stores.add(c)
                    for brand in food_item["brands"].split(","):
                        c, created = Brand.objects.get_or_create(name=brand)
                        new_food_item.brands.add(c)
                else:
                    raise IntegrityError
            except IntegrityError:
                self.stdout.write(
                    "the food item "
                    + food_item["product_name"]
                    + " is already present in DB.\n"
                )
            else:
                pass
        self.stdout.write(str(i) + " food items were added to the database.\n")
