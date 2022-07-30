from django.contrib import admin

from review.models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'description', 'category')


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
