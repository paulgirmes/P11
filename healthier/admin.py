""" 
Model registering for Django admin interface
"""

from django.contrib import admin
from .models import Food_item, Store, Brand

admin.site.register(Food_item)
admin.site.register(Store)
admin.site.register(Brand)
