from django.contrib import admin

# Register your models here.
from .models import Section, Comment, Listing

admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Listing)