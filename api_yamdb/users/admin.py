from django.contrib import admin

from .models import User, VerificationEmailKey

admin.site.register(User)
admin.site.register(VerificationEmailKey)
