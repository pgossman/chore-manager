from django.contrib import admin

from .models import Chore, ChoreAssignment, ChoreInstance, Photo

admin.site.register(Chore)
admin.site.register(ChoreAssignment)
admin.site.register(ChoreInstance)
admin.site.register(Photo)
