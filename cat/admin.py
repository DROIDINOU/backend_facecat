from django.contrib import admin
from .models import CustomUser, Cats,Messages, Points, Fun_Categories

admin.site.register(Cats)
admin.site.register(CustomUser)
admin.site.register(Messages)
admin.site.register(Points)
admin.site.register(Fun_Categories)

# Register your models here.
