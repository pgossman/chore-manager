from django.contrib import admin

from .models import Chore, ChoreAssignment, ChoreInstance

admin.site.register(Chore)
admin.site.register(ChoreAssignment)
admin.site.register(ChoreInstance)
