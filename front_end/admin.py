from django.contrib import admin
from front_end.models import Film, Actor, Director, Writer

# Register your models here.

admin.site.register(Film)

admin.site.register(Actor)

admin.site.register(Director)

admin.site.register(Writer)