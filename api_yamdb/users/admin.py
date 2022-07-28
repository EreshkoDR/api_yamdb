from django.contrib import admin
from users.models import User, VerificationEmailKey

admin.site.register(User)
admin.site.register(VerificationEmailKey)
