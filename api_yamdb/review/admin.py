from django.contrib import admin

from review.models import Category, Comment, Genre, Review, Title

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
