from django.contrib import admin
from .models import Election, Option, Voter, Vote

admin.site.register(Election)
admin.site.register(Option)
admin.site.register(Voter)
admin.site.register(Vote)