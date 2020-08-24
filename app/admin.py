from django.contrib import admin

from .models import Chore, ChoreInstance

admin.site.register(Chore)
admin.site.register(ChoreInstance)
