"""
Healthier app models
"""

from random import choice
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Food_item(models.Model):
    open_food_facts_url = models.URLField(max_length=400)
    name = models.CharField(max_length=200)
    energy_100g = models.CharField(max_length=20)
    nutri_score_fr = models.CharField(
        max_length=1, choices=[("a", "a"), ("b", "b"), ("c", "c"), ("d", "d")]
    )
    nova_grade = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])
    image_url = models.URLField(max_length=400)
    id_open_food_facts = models.BigIntegerField(unique=True)
    stores = models.ManyToManyField(Store)
    brands = models.ManyToManyField(Brand)
    categories = models.ManyToManyField(Category)
    favoris = models.ManyToManyField(User)
    image_nutrition_url = models.URLField(max_length=400)
    def __str__(self):
        return self.name

    @staticmethod
    def get_favorites(username):
        favorites = Food_item.objects.filter(favoris__username=username)
        if favorites.exists():
            return favorites
        else:
            return False

    @staticmethod
    def save_favorites(food_id, user):
        try:
            f = Food_item.objects.get(id=food_id)
            f.favoris.get(username=user.username)
            return {"result": "already existing", "status": False}
        except ObjectDoesNotExist:
            try:
                f.favoris.add(user)
                return {"result": "added", "status": True}
            except:
                return {"result": "unforeseen exception", "status": False}
        else:
            return {"result": "unforeseen exception", "status": False}

    @staticmethod
    def get_searched_food_Item(food_name=None, food_id=None):
        if food_id == None:
            Items_found, number_items_found = Food_item.search(food_name)
            if number_items_found == 1:
                if type(Items_found) == models.QuerySet:
                    Items_found = list(Items_found)[0]
            elif number_items_found > 1:
                return {
                    "status": "choice_to_make",
                    "replacement_items": None,
                    "to_be_replaced_item": Items_found,
                }
            else:
                return {
                    "status": "not_found",
                    "replacement_items": None,
                    "to_be_replaced_item": None,
                }
        else:
            Items_found = Food_item.objects.get(id=food_id)
        replacement = Food_item.replace(Items_found)
        if replacement[0] == True:
            return {
                "status": "ok",
                "replacement_items": replacement[1],
                "to_be_replaced_item": Items_found,
            }
        else:
            replacement = Food_item.replace(Items_found, status="nutri-only")
            if replacement[0] == True:
                return {
                    "status": "ok",
                    "replacement_items": replacement[1],
                    "to_be_replaced_item": Items_found,
                }
            else:
                return {
                    "status": "no_replacement",
                    "replacement_items": None,
                    "to_be_replaced_item": Items_found,
                }

    @staticmethod
    def search(food_name):
        try:
            f = Food_item.objects.get(name__icontains=food_name)
            return (f, 1)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            f = (
                Food_item.objects.filter(name__icontains=food_name)
                .order_by("name")
                .distinct("name")
            )
            return (f, f.all().count())

    @staticmethod
    def replace(food_item, status=None):
        categories = list(food_item.categories.all())
        if status == None:
            replacements = {
                Food_item.objects.filter(
                    categories__name=category,
                    nutri_score_fr__lt=food_item.nutri_score_fr,
                    nova_grade__lt=food_item.nova_grade,
                ).order_by(
                    "nutri_score_fr", "nova_grade",
                )
                for category in categories
            }
        elif status == "nutri-only":
            replacements = {
                Food_item.objects.filter(
                    categories__name=category,
                    nutri_score_fr__lt=food_item.nutri_score_fr,
                ).order_by("nutri_score_fr", "nova_grade")
                for category in categories
            }
        query = []
        {
            query.append(replacement)
            for replacement in replacements
            if replacement.exists()
        }
        cat_number = len(query)
        results = []
        if cat_number > 0:
            replacement_foods = query[0]
            if cat_number > 1:
                i = 0
                while i < cat_number - 2:
                    intersect = query[i].intersection(query[i + 1])
                    if intersect.exists():
                        results.append(intersect)
                    i += 1
                if len(results) > 0:
                    replacement_foods = results[0]
                    x = 0
                    results_choices = []
                    if len(results) > 1:
                        while x < len(results) - 2:
                            result = results[x].intersection(results[x + 1])
                            if result.exists():
                                results_choices.append(result)
                            x += 1
                        if len(results_choices) > 0:
                            replacement_foods = choice(results_choices)
                            return (True, replacement_foods)
                        else:
                            return (True, replacement_foods)
                    else:
                        return (True, replacement_foods)
                else:
                    return (True, replacement_foods)
            else:
                return (True, replacement_foods)
        else:
            return (False, None)

