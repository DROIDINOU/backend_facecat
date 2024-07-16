from django.contrib import admin
from .models import CustomUser, Cats,Messages

admin.site.register(Cats)
admin.site.register(CustomUser)
admin.site.register(Messages)

# Register your models here.
